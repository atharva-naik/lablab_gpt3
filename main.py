import os
import uuid
import openai
import uvicorn
from typing import *
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import convert_to_audio_pyttsx3 as convert

app = FastAPI()
load_dotenv()

app.mount("/voices", StaticFiles(directory="voices", html=True), name="voices")
con_context = []

openai.api_key = os.getenv("OPENAI_API_KEY")
character_to_desc_mapping = {}

def tts_dummy(res: str):    
    return "voices/Brief01.ogg"

@app.get("/")
def welcome():
    return f"Hi! Welcome to the ModMax Beta!"

@app.get("/init")
def init_new_character_session(desc: str):
    global character_to_desc_mapping
    id = str(uuid.uuid4())
    print(f"\x1b[33;1minit new character session\x1b[0m")
    print(f"id: {id}")
    print(f"desc: {desc}")
    character_to_desc_mapping[id] = desc

    return id

@app.get("/reset_character_desc")
def reset_character_desc_by_id(id: str, desc: str):
    global character_to_desc_mapping
    print(f"\x1b[31;1mreset character desc for {id}\x1b[0m")
    old_desc = character_to_desc_mapping[id]
    print(f"old desc: {old_desc}")
    character_to_desc_mapping[id] = desc
    print(f"new desc: {desc}")

    return {"old_desc": old_desc, "status": "Success", "new_desc": desc}

@app.get("/prompt")
def gpt3_simple_prompt_response(query: str, char_id: str):
    global character_to_desc_mapping
    desc = character_to_desc_mapping.get(char_id, "")
    print("prompt for GPT3:", desc+"\n\n"+query)
    # prompt=desc+"\n\n".join(con_context)+"\n\n"+query
    prompt=desc+"\n\n"+query
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
    # con_context.append(query)
    # con_context.append(response["choices"][0]["text"])

    #convert.synthesize_text({'text': response["choices"][0]["text"], 'id': response["id"]})
    return {'text': response["choices"][0]["text"], 'id': response["id"]}

@app.get("/prompt_tts")
def gpt3_prompt_response_with_voice(query: str, char_id: str):
    res_json = gpt3_simple_prompt_response(query, char_id)
    tts_path = convert.synthesize_text(res_json)
    
    return {"text": res_json['text'], "tts_url": tts_path}

@app.get("/reset")
def reset():
    # global con_context
    # con_context = []
    return ""

"""
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
"""

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="debug")


