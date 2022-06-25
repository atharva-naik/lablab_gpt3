

def synthesize_text(respone_object):
    import pyttsx3
    import re

    #audio_title = re.sub('\n', '', respone_object['text'])[0:20]
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    #engine.say(text)
    #engine.save_to_file(respone_object['text']), 'voices/{}.ogg'.format(audio_title))
    engine.save_to_file(respone_object['text'], respone_object['id'] + '.ogg')
    engine.runAndWait()





#text2 ="\n\n Miller is the commander of Combat Technology Research Group (CTRG) Group 14, a multi-national NATO black ops unit. As Group 14's leader, Miller's first and foremost priority was the retrieval of a CSAT seismic weapon of mass destruction that was known only by its codename of "Project Eastwind". For nine years, his team was based on the Mediterranean island nation of the Republic of Altis and Stratis. Under his command, they initially spent five years embedded alongside the anti-coup Altian government Loyalists while also funnelling smuggled arms to the faction. Following the conclusion of the civil war with the signing of the Jerusalem Cease Fire agreement, his team's focus shifted to assisting the successors of the Loyalists"
id = 'test_id'
text ="\n\n Miller is the commander of Combat"
synthesize_text({'text': text, 'id': id})