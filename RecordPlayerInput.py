import os
import json
import pathlib
import keyboard
import requests
import urllib.parse
from typing import *

# TODO: test this function on a Soham's windows system
def downloadTTSFile(url: str, target_destination: str="/downloaded", 
                    fname: Union[str, None]=None) -> str:
    # create target folder if it doesn't exist, ignore otherwise.
    os.makedirs(target_destination, exist_ok=True)
    if fname is None:
        fname = pathlib.Path(target_destination).name
    # final relative path name.
    fname = os.path.join(target_destination, fname)
    content = requests.get(url).content
    # write file to target destination folder.
    with open(fname, "wb") as f:
        f.write(content)
    # return the relative path name.
    return fname

# The event listener will be running in this block
def listenForForwardSlash(start_delim='/', description='', domain='http://localhost:8000', target_destination='downloaded/'):
    while True:
        keyboard.wait(start_delim)
        keyboard.read_key()  # to read first slash
        print(f"'{start_delim}' was pressed. Will now start recording the keys.")
        text = ' '.join(list(keyboard.get_typed_strings(keyboard.record(until='enter', suppress=False, trigger_on_release=False), allow_backspace=True)))
        print("finalv2: ", text)
        safe_string = urllib.parse.quote_plus(description)
        print(f'Sent Request. Waiting for response...')
        r = requests.get(
            f'{domain}/prompt_tts?desc={safe_string}&query=%22What%20does%20Miller%20do%22', params={'query': text})
        print(f'Response received.')
        response_json = json.loads(r.text)
        print(response_json['text'])

        # absolute tts URL.
        abs_tts_url = os.path.join(domain, response_json["tts_url"])
        saved_path = downloadTTSFile(abs_tts_url, target_destination)
        print(f"Speech file saved at {saved_path}")
# with keyboard.Events() as events:
#     for event in events:
#         if event.key == keyboard.Key.enter:
#             break
#         else:
#             print(event.key)
#             if event.key == keyboard.Key.slash:
#                 with keyboard.Record() as rec:
#                     for event in rec:
#                         if event.key == keyboard.Key.enter:
#                             break
#                         else:
#                             print(event.key)
#                             if event.key == keyboard.Key.slash:
#                                 break
#                             else:
#                                 continue
#                 print(rec.text)
#                 import requests
#         r = requests.get(
#             'https://ebed-142-126-69-97.ngrok.io/prompt?desc=%22Miller%20is%20the%20commander%20of%20Combat%20Technology%20Research%20Group%20(CTRG)%20Group%2014,%20a%20multi-national%20NATO%20black%20ops%20unit.%20As%20Group%2014%27s%20leader,%20Miller%27s%20first%20and%20foremost%20priority%20was%20the%20retrieval%20of%20a%20CSAT%20seismic%20weapon%20of%20mass%20destruction%20that%20was%20known%20only%20by%20its%20codename%20of%20%22Project%20Eastwind%22.%20For%20nine%20years,%20his%20team%20was%20based%20on%20the%20Mediterranean%20island%20nation%20of%20the%20Republic%20of%20Altis%20and%20Stratis.%20Under%20his%20command,%20they%20initially%20spent%20five%20years%20embedded%20alongside%20the%20anti-coup%20Altian%20government%20Loyalists%20while%20also%20funnelling%20smuggled%20arms%20to%20the%20faction.%20Following%20the%20conclusion%20of%20the%20civil%20war%20with%20the%20signing%20of%20the%20Jerusalem%20Cease%20Fire%20agreement,%20his%20team%27s%20focus%20shifted%20to%20assisting%20the%20successors%20of%20the%20Loyalists.%20The%20group%20called%20itself%20the%20%22Freedom%20and%20Independence%20Army%22%20(FIA)%20and%20had%20risen%20to%20retake%20the%20country%20from%20the%20oppression%20of%20the%20victorious%20hardline%20Altian%20government%20led%20by%20Georgious%20Akhanteros.%20Miller%20held%20ties%20with%20the%20guerilla%20leader%20Kostas%20Stavrou,%20and%20secretly%20provided%20strategic/tactical%20planning%20for%20the%20group%20while%20his%20team%20(unbeknownst%20to%20the%20guerillas)%20continued%20their%20search%20for%20the%20WMD.%20He%20went%20by%20the%20radio%20callsigns%20of%20Falcon-1%20and%20later%20on,%20also%20as%20Keystone.%22&query=%22What%20does%20Miller%20do%22'
#             , params={'query': rec.text})
#         print(r.text)
#                 break
#             else:
#                 continue
if __name__ == "__main__":
    listenForForwardSlash(description="""Anne was born in Frankfurt, Germany. In 1934, when she was four and a half, her family moved to Amsterdam, Netherlands, after Adolf Hitler and the Nazi Party gained control over Germany. She spent most of her life in or around Amsterdam. By May 1940, the Franks were trapped in Amsterdam by the German occupation of the Netherlands. Anne lost her German citizenship in 1941 and became stateless. As persecutions of the Jewish population increased in July 1942, they went into hiding in concealed rooms behind a bookcase in the building where Anne's father, Otto Frank, worked. Until the family's arrest by the Gestapo on 4 August 1944, Anne kept a diary she had received as a birthday present, and wrote in it regularly.""")
