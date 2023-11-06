import os

import llama_cpp

from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def load_model(model_name, 
               temperature=0):
    
    if model_name == "llama-13b":
        max_tokens=4096
        model_path = os.path.join(
                os.path.expanduser("~"),
                ".cache/gpt4all/llama-2-13b.Q5_K_M.gguf")
    elif model_name == "codellama-13b":
        max_tokens=4096
        model_path = os.path.join(
                os.path.expanduser("~"),
                ".cache/gpt4all/codellama-13b-instruct.Q5_K_M.gguf")
    else:
        max_tokens=2048
        model_path = os.path.join(
                os.path.expanduser("~"),
                ".cache/gpt4all/mistral-7b-instruct-v0.1.Q4_0.gguf")
    
    if not os.path.exists(model_path):
        pass
        
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    
    if llama_cpp.GGML_USE_CUBLAS:
        # create model
        llm = LlamaCpp(
            model_path=model_path,
            n_gpu_layers=80,
            n_batch=1024,
            temperature=temperature,
            max_tokens=max_tokens,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            top_p=1,
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
            )
    else:
        llm = LlamaCpp(
            model_path=model_path,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
            )
    return llm
