import os
import openai
from typing import *
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel

app = FastAPI()
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/prompt")
def gpt3_simple_prompt_response(text: str):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}