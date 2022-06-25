

def synthesize_text(text):
    import pyttsx3
    import re
    
    audio_title = re.sub('\n', '', text)[0:20]

    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    #engine.say(text)
    engine.save_to_file(text, '{}.ogg'.format(audio_title))
    engine.runAndWait()




text ='\n\n Miller is the commander of Combat Technology Research Group (CTRG) Group 14'
synthesize_text(text)