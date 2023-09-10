import os
import re
import random
from typing import Tuple, List
import requests

from flask import Flask, jsonify, request

from dff.script import TRANSITIONS, RESPONSE, Context, Message, PRE_TRANSITIONS_PROCESSING, PRE_RESPONSE_PROCESSING
import dff.script.conditions as cnd
import dff.script.labels as lbl
import dff.script.responses as rsp

from dff.pipeline import Pipeline
from dff.utils.testing.common import (
    is_interactive_mode,
    run_interactive_mode,
)


USE_LLAMA = True

def req(query):
    #query = "В вагоне 2М62У, я нажимаю кнопку “Пуск дизеля”, а у меня маслопрокачивающий насос не работает."
    res = requests.post("http://127.0.0.1:8128/model", json={"query": query})
    if res.status_code == 200:
        otvet = res.json()
        if otvet and otvet[0]:
            return otvet[0][0]
    return []


def llama_request(dialog_history, retrieved_line):
    if len(retrieved_line) == 4:
        fault = retrieved_line[1]
        cause = retrieved_line[2]
        solution = retrieved_line[3]
    else:
        fault=""
        cause=""
        solution=""
    res = requests.post(
        "http://127.0.0.1:8129/model",
        json={"dialog_history": dialog_history, "fault": fault, "cause": cause, "solution": solution}
    )
    if res.status_code == 200:
        return res.json()["response"]
    return ""


def get_otvet(ctx: Context, pipe: Pipeline, *args, **kwargs):
    reqs = ctx.requests
    responses = ctx.responses
    query = ctx.last_request.text
    dialog_history = []

    for i in range(min(len(reqs), len(responses))):
        dialog_history += [reqs[i].text, responses[i].text]
    dialog_history.append(query)
    try:
        new_user_request = req(query)
        if not USE_LLAMA and new_user_request:
            bot_otvet = new_user_request[3]
        else:
            bot_otvet = llama_request(dialog_history, new_user_request)

    except Exception as e:
        bot_otvet = ""
        print(f"error: {e}")
    return Message(text=bot_otvet)


def fallback_trace_response(ctx: Context, pipe: Pipeline, *args, **kwargs) -> Message:
    misc = {}    
    return Message(misc=misc)


bot_script = {
    "dialog_flow": {
        "start_node": {  # This is an initial node, it doesn't need a `RESPONSE`.
            RESPONSE: Message(),
            TRANSITIONS: {"otvet": cnd.true()},
        },
        "otvet":{
            RESPONSE: get_otvet,
            TRANSITIONS: {lbl.repeat(): cnd.true()},
        },

        "fallback_node": {  # We get to this node
            # if an error occurred while the agent was running.
            RESPONSE: fallback_trace_response,
            TRANSITIONS: {"start_node": cnd.true()},
        },
    }
}


pipeline = Pipeline.from_script(
    bot_script,
    start_label=("dialog_flow", "start_node"),
    fallback_label=("dialog_flow", "fallback_node"),
)


# handler requests
def turn_handler(in_request: Message, pipeline: Pipeline) -> Tuple[Message, Context]:
    # Pass the next request of user into pipeline and it returns updated context with actor response
    ctx = pipeline(in_request, 0)
    # Get last actor response from the context
    out_response = ctx.last_response
    # The next condition branching needs for testing
    return out_response, ctx


SERVICE_PORT = 5130
app = Flask(__name__)

default_phrases = ["Хорошо, я подумаю, как устранить вашу неисправность.", "Я был рад вам помочь.", "Интересный вопрос, но я не знаю на него ответ."]

@app.route("/model", methods=["POST"])
def model():
    try:
        dialog_history = request.json["dialog_history"]
        in_request = dialog_history[-1]
        labels = {n: ("dialog_flow", "otvet") for n in range(len(dialog_history) // 2)}
        requests = {n: Message(text=dialog_history[2*n]) for n in range(len(dialog_history) // 2)}
        responses = {n: Message(text=dialog_history[2*n + 1]) for n in range(len(dialog_history) // 2)}
        cur_ctx = {"id": 0, "labels": labels, "requests": requests, "responses": responses, "misc": {}, "validation": False, "framework_states": {}}
        pipeline.context_storage = {0: Context.cast(cur_ctx)}
        out_response_message, ctx = turn_handler(Message(text=in_request), pipeline)
        out_response = out_response_message.text
    except Exception as e:
        print(e)
        out_response = random.choice(default_phrases)
        print(f"error in response generation: {e}")
    if not out_response:
        out_response = random.choice(default_phrases)
    return jsonify({"response": out_response})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=SERVICE_PORT)
