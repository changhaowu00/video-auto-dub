import os
import pyttsx3
from pydub import AudioSegment
import time

# Function to parse the subtitle file
def parse_subtitles(file_path):
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        index = 0
        while index < len(lines):
            # Parse the number
            num = lines[index].strip()
            index += 1
            # Parse the time range (start --> end)
            time_range = lines[index].strip()
            start_time, end_time = time_range.split(' --> ')
            index += 1
            # Parse the subtitle text
            subtitle_text = lines[index].strip()
            index += 2
            subtitles.append((num, start_time, end_time, subtitle_text))
    return subtitles

# Function to convert text to speech and return an AudioSegment
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'temp_audio.wav')
    engine.runAndWait()
    
    # Load the generated audio file
    audio = AudioSegment.from_wav('temp_audio.wav')
    return audio

# Function to adjust audio duration
def adjust_audio_duration(audio, start_time, end_time):
    # Calculate the duration in milliseconds
    start_ms = convert_time_to_ms(start_time)
    end_ms = convert_time_to_ms(end_time)
    duration_ms = end_ms - start_ms
    
    # Adjust the audio to match the required duration
    if len(audio) < duration_ms:
        silence = AudioSegment.silent(duration=duration_ms - len(audio))
        audio = audio + silence
    elif len(audio) > duration_ms:
        audio = audio[:duration_ms]
    
    return audio

# Helper function to convert time format HH:MM:SS,SSS to milliseconds
def convert_time_to_ms(time_str):
    h, m, s = time_str.split(':')
    seconds, ms = s.split(',')
    ms = int(ms)
    total_ms = int(h) * 3600000 + int(m) * 60000 + int(seconds) * 1000 + ms
    return total_ms

# Function to generate the complete audio file based on the subtitles
def generate_audio_from_subtitles(subtitle_file, out_file):
    subtitles = parse_subtitles(subtitle_file)
    
    final_audio = AudioSegment.silent(duration=0)  # Start with an empty audio
    for subtitle in subtitles:
        num, start_time, end_time, text = subtitle
        
        # Generate speech for the subtitle text
        audio = text_to_speech(text)
        
        # Adjust the duration of the audio
        audio = adjust_audio_duration(audio, start_time, end_time)
        
        # Add the audio to the final track
        final_audio += audio
    
    # Export the final audio file
    final_audio.export(out_file, format="wav")
    print("Audio file generated successfully in "+ out_file)

# Example usage
out3 = os.getcwd() + "/output_files/" + "tts_es_subtitles.txt"
out_file = os.getcwd() + "/audios/" + "subtitles_audio.wav"
generate_audio_from_subtitles(out3, out_file)
