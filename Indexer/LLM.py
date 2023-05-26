import torch
from langchain.llms.base import LLM
from transformers import LlamaTokenizer, LlamaForCausalLM
from typing import Optional, List, Mapping, Any

class CustomLLM(LLM):
    tokenizer : LlamaTokenizer
    model : LlamaForCausalLM
    
    def loadmodel(self):
        self.model.to(self.device)
        
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=2048, padding = False, truncation = True)
        input_length = inputs.input_ids.shape[1]

        with torch.autocast(self.model.device.type):
            output = self.model.generate(inputs.input_ids.to(self.model.device),
                                         attention_mask = inputs.attention_mask.to(self.model.device), 
                                        max_length=min(2048, len(inputs.input_ids[0])+1024), 
                                         do_sample=True, 
                                         temperature = 0.001)
        torch.cuda.empty_cache()
        
        token = output[0, input_length:]
        response = self.tokenizer.decode(token, skip_special_tokens=True)
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"name_of_model": self.model.config._name_or_path}

    @property
    def _llm_type(self) -> str:
        return "custom"