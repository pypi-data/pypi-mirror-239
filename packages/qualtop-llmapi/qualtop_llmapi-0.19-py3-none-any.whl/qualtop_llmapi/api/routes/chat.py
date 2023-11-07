import logging
import time
from typing import Dict, List
import tiktoken

from fastapi import APIRouter, Depends, Response, Security, status
from pydantic import BaseModel, Field

from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage

import qualtop_llmapi.models.loading as loading
import qualtop_llmapi.models.single_prompt as single_prompt

llm = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

### This should follow https://github.com/openai/openai-openapi/blob/master/openapi.yaml
class ChatCompletionMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description='The model to generate a completion from.')
    messages: List[ChatCompletionMessage] = Field(..., description='The model to generate a completion from.')


class ChatCompletionChoice(BaseModel):
    message: ChatCompletionMessage
    index: int
    finish_reason: str


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = 'text_completion'
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage


router = APIRouter(prefix="/chat", tags=["Completions Endpoints"])

# Message formatting for LangChain
def format_messages(messages):
    formatted_messages = []
    for message in messages:
        formatted_messages.append((message['role'], message["content"]))
    return ChatPromptTemplate.from_messages(formatted_messages)

# Count tokens
def num_tokens(text, model):
    """Return the number of tokens in a string."""
    if "llama" in model or "mistral" in model:
        encoding = tiktoken.get_encoding("gpt2")
    else:
        encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

@router.post("/completions", response_model=ChatCompletionResponse)
async def chat_completion(request: ChatCompletionRequest):
    '''
    Completes a LLM model response.
    '''
    req_dict = request.dict()
    messages = req_dict["messages"]
    formatted_messages = format_messages(messages)
    model_name = req_dict["model"]
    
    global llm
    # Load model
    if not llm:
        llm = loading.load_model(model_name)

    token_count = num_tokens(formatted_messages.format(), model_name)
    print(f"\nTokens: {token_count}\n")
    try:
        answer = single_prompt.ask(formatted_messages, llm)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, 
                            detail="Model not found.")

    choices = [ChatCompletionChoice(message=ChatCompletionMessage(role="assistant",
                                                                  content=answer),
                                    index=0,
                                    finish_reason="stop")]
   
    # Get measures
    prompt_tokens = num_tokens(formatted_messages.format(), model_name)
    completion_tokens = num_tokens("Assistant: " + answer, model_name)
    total_tokens = prompt_tokens + completion_tokens

    return ChatCompletionResponse(
        id="chatcmpl-abc123",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=choices,
        usage={'prompt_tokens': prompt_tokens, 
               'completion_tokens': completion_tokens, 
               'total_tokens': total_tokens},
    )
