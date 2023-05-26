import gradio as gr
import time
from typing import Any
class IndexingUI:
    
    query_engine: Any

    def user(self, user_text, history):
        return "", history + [[user_text, None]]

    def generate(self, history):
        result = self.query_engine(history[-1][0])
        history[-1][1] = ""
        for character in str(result.response):
            history[-1][1] += character
            time.sleep(0.05)
            yield history
        return history
    
    def launch(self, host='localhost', port=8888):
        with gr.Blocks(title='Amazon Bestsellers', theme=gr.themes.Soft()) as iface:
            with gr.Row():
                gr.Markdown(
                    "# Find bestselling products on Amazon"
                )
            
            with gr.Column():
                chatbot = gr.Chatbot()
                input_text = gr.Textbox(placeholder="Find your best product")
                input_text.submit(
                    self.user, [input_text, chatbot], [input_text, chatbot], queue = False
                ).then(
                    self.generate, chatbot, chatbot
                )

        iface.queue()
        iface.launch(
            server_name = host,
            server_port = port)        
