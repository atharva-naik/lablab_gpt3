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
    domain_name = "http://localhost:8000"
    char_id = add_character("""Anne was born in Frankfurt, Germany. In 1934, when she was four and a half, her family moved to Amsterdam, Netherlands, after Adolf Hitler and the Nazi Party gained control over Germany. She spent most of her life in or around Amsterdam. By May 1940, the Franks were trapped in Amsterdam by the German occupation of the Netherlands. Anne lost her German citizenship in 1941 and became stateless. As persecutions of the Jewish population increased in July 1942, they went into hiding in concealed rooms behind a bookcase in the building where Anne's father, Otto Frank, worked. Until the family's arrest by the Gestapo on 4 August 1944, Anne kept a diary she had received as a birthday present, and wrote in it regularly.""")
    response_text, saved_audio_path = send_player_input_windows(char_id=char_id)
    characters_info = [{
        "class_name": "Brief_SQL_Line_1",
        "text": response_text.strip(),
        "speech_path": saved_audio_path.strip(),
        "actor_name": "SQL"
    }]
    generate_bibk(characters_info, target_directory="C:\\Users\\soham\\Desktop\\lablab_gpt3\\bibks", filename="brief_demo.bibk")
