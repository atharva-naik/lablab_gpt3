import os
import openai
from typing import *
from fastapi import FastAPI
from dotenv import load_dotenv
from pandas import array
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import convert_to_audio_pyttsx3 as convert

app = FastAPI()
load_dotenv()

app.mount("/voices", StaticFiles(directory="voices", html=True), name="voices")
con_context = []

openai.api_key = os.getenv("OPENAI_API_KEY")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None



def tts_dummy(res: str):
    
    return "voices/Brief01.ogg"

@app.get("/prompt")
def gpt3_simple_prompt_response(query: str, desc: str):
    print(con_context)
    prompt=desc+"\n\n".join(con_context)+"\n\n"+query
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    con_context.append(query)
    con_context.append(response["choices"][0]["text"])

    #convert.synthesize_text({'text': response["choices"][0]["text"], 'id': response["id"]})
    return {'text': response["choices"][0]["text"], 'id': response["id"]}

@app.get("/prompt_tts")
def gpt3_prompt_response_with_voice(query: str, desc: str):
    res = gpt3_simple_prompt_response(query, desc)
    tts_path = tts_dummy(res)
    
    return {"text": res, "tts_url": tts_path}

@app.get("/reset")
def reset():
    global con_context
    con_context = []
    return ""

"""
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
"""




