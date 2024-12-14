import os
import whisper
from utils import *
import re

# Transcribe and translate the video file (Chinese to Spanish)
model = whisper.load_model("turbo")
input_audio = os.getcwd() + "/videos/" + "venom1.mp4"
ouput_subtitles = os.getcwd() + "/output_files/" + "tts_ch_subtitles.txt"
# generate_subtitles(input_audio, ouput_subtitles, model)



#------------------- Caption extraction ------------------------
# Input and output file paths
input_file = ouput_subtitles
output_file = os.getcwd() + "/output_files/" + "raw_tts_ch_subtitles.txt"

# Read the input file
with open(input_file, "r", encoding="utf-8") as file:
    content = file.read()

# Use a regular expression to extract captions
# Captions are lines not containing timestamps or sequence numbers
lines = content.splitlines()
captions = []
for line in lines:
    if not re.match(r"^\d+$", line) and not re.match(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$", line):
        if line.strip():  # Skip empty lines
            captions.append(line)

# Write the captions to the output file
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(captions))

print(f"Captions extracted and saved to {output_file}")


#--------------------- Caption Insertion ----------------------



