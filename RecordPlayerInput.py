import os
import json
import platform
from tarfile import TarError
import keyboard
import requests
import urllib.parse
from typing import *

def downloadTTSFile(url: str, target_destination: str = "/downloaded",
                    fname: Union[str, None] = None) -> str:
    # create target folder if it doesn't exist, ignore otherwise.
    os.makedirs(target_destination, exist_ok=True)
    if fname is None:
        fname = os.path.basename(url)
    # final relative path name.
    fname = os.path.join(target_destination, fname)
    print(f'url: {url}')
    doc = requests.get(url)
    # write file to target destination folder.
    with open(fname, "wb") as f:
        f.write(doc.content)
    # return the relative path name.
    return fname

def add_character(desc: str, domain: str="http://localhost:8000") -> str:
    """Create a new character for a given description and return the character id.
    Args:
        desc (str): character description to be passed to GPT3
        domain (_type_, optional): Domain of the server. Defaults to "http://localhost:8000".
    Returns:
        str: character id
    """
    desc = urllib.parse.quote_plus(desc)
    url = f"{domain}/init?desc={desc}"
    return json.loads(requests.get(url).text)

# platform indpendent part to communicate with ModMax and get text (subtitles) and voice output.
def send_player_input_to_server(text, char_id='', domain='http://localhost:8000', target_destination='downloaded/'):
    print(f"query: {text}")
    query = urllib.parse.quote_plus(text)
    print(f'Sent Request. Waiting for response...')
    r = requests.get(f'{domain}/prompt_tts?char_id={char_id}&query={query}')
    print(f'Response received.')
    response_json = json.loads(r.text)
    text = response_json['text']
    if len(text.strip()) ==0:
        text = "[WARNING: Empty string received as response.]"
    print(text)
    # absolute tts URL.
    tts_url = response_json["tts_url"]
    abs_tts_url = f'{domain}/{tts_url}'
    saved_path = downloadTTSFile(abs_tts_url, target_destination)
    print(f"Speech file saved at {saved_path}")

# keylogger will start after '/'. Only works for Windows.
def send_player_input_windows(start_delim='/', char_id='', domain='http://localhost:8000', target_destination='downloaded/'):
    while True:
        keyboard.wait(start_delim)
        keyboard.read_key()  # to read first slash
        print(f"'{start_delim}' was pressed. Will now start recording the keys.")
        text = ' '.join(list(keyboard.get_typed_strings(keyboard.record(
            until='enter', suppress=False, trigger_on_release=False), allow_backspace=True)))
        send_player_input_to_server(text, char_id=char_id, domain=domain, 
                                    target_destination=target_destination)

# Keylogger for linux.
class LinuxKeyLogger:
    def __init__(self):
        import pyxhook
        # text recorded till now.
        self.recorded_text: str=""
        # create a hook manager object
        self.hook = pyxhook.HookManager()
        self.hook.KeyDown = self.onKeyPress
        # set hook.
        self.hook.HookKeyboard()
        self.return_callback = None
        self.return_callback_args = []
        self.return_callback_kwargs = {}

    def setReturnCallback(self, func, args: list=[], kwargs: dict={}):
        self.return_callback = func
        self.return_callback_args = args
        self.return_callback_kwargs = kwargs

    def start(self):
        import pyxhook
        try:
            self.hook.start()
        except KeyboardInterrupt:
            exit("\x1b[31;1mexited\x1b[0m on \x1b[1mKeyboardInterrupt\x1b[0m")
        except Exception as ex:
            msg = 'Error while catching events:\n {}'.format(ex)
            pyxhook.print_err(msg)

    def text(self):
        return self.recorded_text

    def onKeyPress(self, event):
        evenText = str(event.Key)
        if evenText == "BackSpace":
            self.recorded_text = self.recorded_text[:-1]
        elif evenText == "space":
            self.recorded_text += " "
        elif evenText == "Return":
            self.return_callback(
                self.recorded_text,
                *self.return_callback_args, 
                **self.return_callback_kwargs
            )
        elif evenText == "question":
            self.recorded_text += "?"
        elif len(evenText) == 1:
            self.recorded_text += f"{event.Key}"
        print(" ", end="\r")
        print(f"DEBUG: {self.recorded_text}", end="\r") # DEBUG

# for testing send player input on linux.
def send_player_input_linux(start_delim='/', char_id='', domain='http://localhost:8000', target_destination='downloaded/'):
    linux_key_logger = LinuxKeyLogger()
    linux_key_logger.setReturnCallback(
        send_player_input_to_server,
        kwargs={
            "char_id": char_id, "domain": domain,
            "target_destination": target_destination,
        }
    )
    linux_key_logger.start()
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
    char_id = add_character("""Anne was born in Frankfurt, Germany. In 1934, when she was four and a half, her family moved to Amsterdam, Netherlands, after Adolf Hitler and the Nazi Party gained control over Germany. She spent most of her life in or around Amsterdam. By May 1940, the Franks were trapped in Amsterdam by the German occupation of the Netherlands. Anne lost her German citizenship in 1941 and became stateless. As persecutions of the Jewish population increased in July 1942, they went into hiding in concealed rooms behind a bookcase in the building where Anne's father, Otto Frank, worked. Until the family's arrest by the Gestapo on 4 August 1944, Anne kept a diary she had received as a birthday present, and wrote in it regularly.""")
    osname = platform.system()
    print(f"on platform: {osname}")
    if osname == "Windows":
        send_player_input_windows(char_id=char_id)
    elif osname == "Linux":
        send_player_input_linux(char_id=char_id)
        