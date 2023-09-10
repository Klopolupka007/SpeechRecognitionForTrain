# pip install llama-cpp-python fire requests

import copy
import os
import requests
from typing import List

import fire
import uvicorn
from fastapi import FastAPI
from llama_cpp import Llama
from pydantic import BaseModel


# Weights of quantized Saiga download from the link:
# https://huggingface.co/IlyaGusev/saiga2_7b_gguf/resolve/main/ggml-model-q3_K.gguf

SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}


def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    return get_message_tokens(model, **system_message)


if not os.path.exists("saiga_checkpoints"):
    os.mkdir("saiga_checkpoints")

if not os.path.exists("saiga_checkpoints/ggml-model-q3_K.gguf"):
    file_resp = requests.get("https://huggingface.co/IlyaGusev/saiga2_7b_gguf/resolve/main/ggml-model-q3_K.gguf")
    if file_resp.status_code == 200:
        with open("saiga_checkpoints/ggml-model-q3_K.gguf", 'wb') as out:
            out.write(file_resp.content)

model_path = "saiga_checkpoints/ggml-model-q3_K.gguf"

n_ctx = 2000
top_k = 30
top_p = 0.9
temperature = 0.2
repeat_penalty = 1.1

model = Llama(model_path=model_path, n_ctx=n_ctx, n_parts=1)

system_tokens = get_system_tokens(model)
tokens = system_tokens
model.eval(tokens)


SERVICE_PORT = 8129
app = FastAPI()

class Payload(BaseModel):
    dialog_history: List[str]
    fault: str
    cause: str
    solution: str


@app.post("/model")
async def generate_response(payload: Payload):
    try:
        dialog_history = payload.dialog_history
        fault = payload.fault
        cause = payload.cause
        solution = payload.solution
        cur_tokens = copy.deepcopy(tokens)
        for n, message in enumerate(dialog_history[:-1]):
            if n % 2 == 0:
                message_tokens = get_message_tokens(model=model, role="user", content=message)
            else:
                message_tokens = get_message_tokens(model=model, role="bot", content=message)
            cur_tokens += message_tokens

        if fault and cause and solution:
            last_user_message = "User: Сгенерируй совет для устранения несправности в разговорной форме, "\
                                f"используя только приведенное описание возможной причины и возможного решения. "\
                                f"Возможная причина: {cause} Возможное решение: {solution}."
        else:
            last_user_message = dialog_history[-1]
        print(f"last user message: {last_user_message}")

        last_message_tokens = get_message_tokens(model=model, role="user", content=last_user_message)
        role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
        cur_tokens += last_message_tokens
        cur_tokens += role_tokens

        generator = model.generate(
            cur_tokens,
            top_k=top_k,
            top_p=top_p,
            temp=temperature,
            repeat_penalty=repeat_penalty
        )

        generated_tokens = []
        for token in generator:
            token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
            generated_tokens.append(token_str)
            if token == model.token_eos():
                break
        response = ''.join(generated_tokens)
    except Exception as e:
        print(e)
        response = "На данный вопрос у меня нет ответа."
        print(f"error: {e}")
    return {"response": response}


uvicorn.run(app, host='0.0.0.0', port=SERVICE_PORT)
