import os
import whisper
from utils import *
import re

# 1 ------------------- Subtitles generation with whisper TTS ----------------------
model = whisper.load_model("turbo")
input_audio = os.getcwd() + "/videos/" + "venom1.mp4"
ouput_subtitles = os.getcwd() + "/output_files/" + "tts_ch_subtitles.txt"
generate_subtitles(input_audio, ouput_subtitles, model)

# 2 ------------------- Extract subtitles into raw_tts_ch_subtitles.txt ------------------------
def extract_captions(input_file, ouput_file):
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

input_file = ouput_subtitles
output_file = os.getcwd() + "/output_files/" + "raw_tts_ch_subtitles.txt"
extract_captions(input_file, output_file)

# 4 ------------------- Translate raw_tts_ch_subtitles.txt into raw_tts_es_subtitles.txt ----------------------

# 5 ------------------- Replace raw_tts_es_subtitles.txt line into captions format in tts_es_subtitles.txt----------------------
def replace_lines(first_file, second_file, out_file):
    # Read the content of the first text file
    with open(first_file, 'r') as file:
        lines_to_replace = file.readlines()

    # Read the content of the second text file (subtitles or text with time codes)
    with open(second_file, 'r') as file:
        subtitles = file.readlines()

    # Prepare an empty list to store the modified subtitles
    modified_subtitles = []
    line_index = 0  # Keeps track of the line number in the 'lines_to_replace' list

    # Iterate through the subtitle file and replace lines where necessary
    for i in range(0, len(subtitles), 4):  # The subtitle file has 4 lines per entry (index, time, text)
        if line_index < len(lines_to_replace):  # Ensure we do not exceed the number of lines to replace
            # Get the current subtitle and replace the text
            subtitle_text = subtitles[i + 2].strip()  # Extract the current subtitle text
            new_line = lines_to_replace[line_index].strip()  # Get the replacement line
            
            # Replace the subtitle text with the new line
            modified_subtitles.append(subtitles[i])  # Add the index
            modified_subtitles.append(subtitles[i + 1])  # Add the time code
            modified_subtitles.append(new_line + '\n')  # Add the new line
            modified_subtitles.append(subtitles[i + 3])  # Add the blank line after each subtitle
            
            line_index += 1  # Move to the next line to replace

    # Write the modified subtitles to a new text file
    with open(out_file, 'w') as file:
        file.writelines(modified_subtitles)

    print("Replacement completed. Check 'output.txt' for the result.")

in1 =os.getcwd() + "/output_files/" + "tts_ch_subtitles.txt"
in2 =os.getcwd() + "/output_files/" + "raw_tts_es_subtitles.txt"
out3 = os.getcwd() + "/output_files/" + "tts_es_subtitles.txt"
replace_lines(in2,in1,out3)

# 6 ------------------- Generate audio -------------------------

