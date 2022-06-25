from typing import Dict


def synthesize_text(response_object: Dict):
    import pyttsx3
    text = response_object['text']
    audio_title = response_object['id']
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # voices[0] is MALE
    engine.setProperty('rate', 150) # voices[0] is MALE
    engine.save_to_file(text, 'voices/{}.ogg'.format(audio_title))
    engine.runAndWait()
    return 'voices/{}.ogg'.format(audio_title)



if __name__ == "__main__":
    text2="\n\n Miller is the commander of Combat Technology Research Group (CTRG) Group 14, a multi-national NATO black ops unit. As Group 14's leader, Miller's first and foremost priority was the retrieval of a CSAT seismic weapon of mass destruction that was known only by its codename of \"Project Eastwind\". For nine years, his team was based on the Mediterranean island nation of the Republic of Altis and Stratis. Under his command, they initially spent five years embedded alongside the anti-coup Altian government Loyalists while also funnelling smuggled arms to the faction. Following the conclusion of the civil war with the signing of the Jerusalem Cease Fire agreement, his team's focus shifted to assisting the successors of the Loyalists"
    id='test_id_123'
    text="Miller is the commander of Combat"
    synthesize_text({'text': text, 'id': id})
