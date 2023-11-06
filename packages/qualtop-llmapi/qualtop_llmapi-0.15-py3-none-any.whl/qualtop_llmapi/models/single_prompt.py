import os

def ask(messages, llm):
    output = llm(messages.format())
    output = " ".join(output.split(":")[1:])
    return output.strip()
