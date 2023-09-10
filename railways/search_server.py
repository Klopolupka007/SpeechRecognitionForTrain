import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from deeppavlov import build_model


SERVICE_PORT = 8128
app = FastAPI()

class Payload(BaseModel):
    query: str

ru_ranker_tfidf_rail = build_model("./ru_ranker_tfidf_rail.json", download=True)

@app.post("/model")
async def model(payload: Payload):
    query = payload.query
    texts_batch, scores_batch = ru_ranker_tfidf_rail([query])
    res_batch = []
    for texts, scores in zip(texts_batch, scores_batch):
        res = []
        for text, score in zip(texts, scores):
            if score > 2:
                res.append(text)
        res_batch.append(res)
    return res_batch


uvicorn.run(app, host='0.0.0.0', port=SERVICE_PORT)
