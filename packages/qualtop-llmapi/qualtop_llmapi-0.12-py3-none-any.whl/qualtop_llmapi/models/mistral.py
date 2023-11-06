import os
from langchain.llms import LlamaCpp

from langchain.prompts import PromptTemplate

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def ask(messages):

    # Process messages
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
    model_path="~/.cache/gpt4all/mistral-7b-instruct-v0.1.Q4_0.gguf",
    temperature=0.7,
    max_tokens=2000,
    top_p=1,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
    )

    output = llm(messages.format())
    output = " ".join(output.split(":")[1:])
    return output.strip()
