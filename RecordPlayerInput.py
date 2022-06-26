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
        self.listening = True
        self.trigger_key_text = ""

    def setTriggerKey(self, trigger_key_text):
        self.trigger_key_text = trigger_key_text

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
        # first check if the key is the trigger key. 
        # If it is then start listening,
        if evenText == self.trigger_key_text:
            self.listening = True
        # if the key wasn't trigger key and listening hasn't been activated yet, ignore.
        if self.listening == False: return
        
        if evenText == "BackSpace":
            self.recorded_text = self.recorded_text[:-1]
        elif evenText == "space":
            self.recorded_text += " "
        # call the callback function with the text and any other needed arguments when return is pressed.
        elif evenText == "Return":
            self.return_callback(
                self.recorded_text,
                *self.return_callback_args, 
                **self.return_callback_kwargs
            )
            # reset recorded text  and listening mode.
            self.recorded_text = ""
            self.listening = False

        elif evenText == "question":
            self.recorded_text += "?"
        elif len(evenText) == 1:
            self.recorded_text += f"{event.Key}"
        print(" ", end="\r")
        print(f"DEBUG: {self.recorded_text}", end="\r") # DEBUG

# for testing send player input on linux.
def send_player_input_linux(start_delim='/', char_id='', domain='http://localhost:8000', target_destination='downloaded/'):
    linux_key_logger = LinuxKeyLogger()
    linux_key_logger.setTriggerKey("slash")
    linux_key_logger.setReturnCallback(
        send_player_input_to_server,
        kwargs={
            "char_id": char_id, "domain": domain,
            "target_destination": target_destination,
        }
    )
    linux_key_logger.start()


if __name__ == "__main__":
    char_id = add_character("""Anne was born in Frankfurt, Germany. In 1934, when she was four and a half, her family moved to Amsterdam, Netherlands, after Adolf Hitler and the Nazi Party gained control over Germany. She spent most of her life in or around Amsterdam. By May 1940, the Franks were trapped in Amsterdam by the German occupation of the Netherlands. Anne lost her German citizenship in 1941 and became stateless. As persecutions of the Jewish population increased in July 1942, they went into hiding in concealed rooms behind a bookcase in the building where Anne's father, Otto Frank, worked. Until the family's arrest by the Gestapo on 4 August 1944, Anne kept a diary she had received as a birthday present, and wrote in it regularly.""")
    osname = platform.system()
    print(f"on platform: {osname}")
    if osname == "Windows":
        send_player_input_windows(char_id=char_id)
    elif osname == "Linux":
        send_player_input_linux(char_id=char_id)
        