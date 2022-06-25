
import json
import os
import sys
import re

#get the json response ive choose a json file here because idk how to parse it directly
json_file = open("brief.json", "r")
json_data = json.load(json_file)

#get the bikb file
bikb_file = open("brief.bikb", "r")
bikb_data = bikb_file.read()

#get the text from the json file
text = json_data["text"]

#get the text from the bikb file
bikb_text = re.search(r'text = "(.*)";', bikb_data).group(1)

#replace the text in the bikb file with the text from the json file
bikb_data = bikb_data.replace(bikb_text, text)

#write the new bikb file
bikb_file = open("brief.bikb", "w")
bikb_file.write(bikb_data)

#close the files
json_file.close()
bikb_file.close()
