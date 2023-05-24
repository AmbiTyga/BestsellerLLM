from LLM import CustomLLM
from transformers import LlamaTokenizer, LlamaForCausalLM
import torch
from llama_index import LangchainEmbedding, GPTVectorStoreIndex, PromptHelper
from llama_index.prompts.prompts import QuestionAnswerPrompt
from llama_index import LLMPredictor, ServiceContext, SimpleMongoReader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

import time
import gradio as gr

if __name__ == "__main__":
    prompt_helper = PromptHelper(
        max_input_size=1024,
        num_output=256,
        max_chunk_overlap=20
    )

    hfemb = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs = {
            'device': torch.device("cuda:0")
        }
    )

    embed_model = LangchainEmbedding(hfemb)

    llm = CustomLLM(
                model = LlamaForCausalLM.from_pretrained("TheBloke/vicuna-7B-1.1-HF", torch_dtype=torch.bfloat16).to(torch.device('cuda:0')),
                tokenizer=LlamaTokenizer.from_pretrained("TheBloke/vicuna-7B-1.1-HF")
            )
    llm_predictor = LLMPredictor(llm=llm)
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, 
        prompt_helper=prompt_helper,
        embed_model=embed_model
    )
    reader = SimpleMongoReader(host='mongodb://localhost',port=27017)
    documents = reader.load_data(
        db_name='amazon', collection_name='bestsellers', field_names=['text'], query_dict={}
    )

    indexer = GPTVectorStoreIndex.from_documents(
        documents=documents,
        service_context=service_context
    )

    QA_template = QuestionAnswerPrompt(
        "USER: Context information is below."
        "\n---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Limiting yourself only to the context above, "
        "answer the question: {query_str}.\n ASSISTANT: "
    )

    query_engine = indexer.as_query_engine(text_qa_template=QA_template)

    def user(user_text, history):
        return "", history + [[user_text, None]]
    
    def generate(history):
        result = query_engine.query(history[-1][0])
        history[-1][1] = ""
        for character in str(result.response):
            history[-1][1] += character
            time.sleep(0.05)
            yield history

    with gr.Blocks(title='Amazon Bestsellers', theme=gr.themes.Soft()) as iface:
        with gr.Row():
            gr.Markdown(
                """
                # Find bestselling products on 
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1200px-Amazon_logo.svg.png" alt="Image" height="40px">
                """
            )
        
        with gr.Row():
            chatbot = gr.Chatbot()
            input_text = gr.Textbox(placeholder="Find your best product")
            input_text.submit(
                user, [input_text, chatbot], [input_text, chatbot], queue = False
            ).then(
                generate, chatbot, chatbot
            )

    iface.queue()
    iface.launch(
        server_name = 'localhost',
        server_port = 8888)