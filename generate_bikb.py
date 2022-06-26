from typing import List
import jinja2
import os
from RecordPlayerInput import add_character, send_player_input_windows


def generate_bibk(characters_info: List, target_directory: str, filename: str):
    bibk_code = jinja2.Template("""class Sentences
{
    {% for dict in characters_info: %}
    class {{dict.class_name}}
	{
		text = "{{dict.text}}";
		speech[] = { "{{dict.speech_path}}" };
		class Arguments {};
		actor = "{{dict.actor_name}}";
	};
    {% endfor %}
};
class Arguments {};
class Special {};
startWithVocal[] = {hour};
startWithConsonant[] = {europe, university};
""").render(characters_info=characters_info)
    print(bibk_code)
    os.makedirs(target_directory, exist_ok=True)
    with open(os.path.join(target_directory, filename), "w") as f:
        f.write(bibk_code)

if __name__ == "__main__":
    domain_name = "https://9d64-49-32-136-100.in.ngrok.io"
    char_id = add_character("""Miller is the commander of Combat Technology Research Group (CTRG) Group 14, a multi-national NATO black ops unit. 
    As Group 14's leader, Miller's first and foremost priority was the retrieval of a CSAT seismic weapon of mass destruction that was known only by its codename of "Project Eastwind". For nine years, 
    his team was based on the Mediterranean island nation of the Republic of Altis and Stratis. 
    Under his command, they initially spent five years embedded alongside the anti-coup Altian government Loyalists while also funnelling smuggled arms to the faction.""", domain = domain_name)
    response_text, saved_audio_path = send_player_input_windows(domain = domain_name, char_id=char_id, target_destination="C:\\Users\\User\\Documents\\Arma 3 - Other Profiles\\SemteX\\missions\\Hackaton1.Altis\\voices")
    characters_info = [{
        "class_name": "Brief_SQL_Line_1",
        "text": response_text.strip(),
        "speech_path": saved_audio_path.strip(),
        "actor_name": "SQL"
    }
    ]
    generate_bibk(characters_info, target_directory="C:\\Users\\User\\Documents\\Arma 3 - Other Profiles\\SemteX\\missions\\Hackaton1.Altis", filename="brief.bikb")
