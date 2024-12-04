# File config
import os
from pydub import AudioSegment
from moviepy import VideoFileClip
from pydub.silence import split_on_silence

FILENAME = "venom1"
INPUT_VIDEO_PATH = os.getcwd() + "/videos/" + FILENAME + ".mp4"
OUTPUT_TEXT_PATH = os.getcwd() + "/output_files/" + FILENAME + ".txt"

def speed_up_audio(input_file, output_file, speed_factor=1.5):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Speed up the audio by changing the playback speed
    # Speed factor > 1 will speed up, < 1 will slow down
    sped_up_audio = audio.speedup(playback_speed=speed_factor)

    # Export the sped-up audio to a new file
    sped_up_audio.export(output_file, format="mp3")

    print(f"Audio saved as {output_file}")

def remove_silence(input_file, output_file, silence_thresh=-40, min_silence_len=1000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Split the audio based on silence
    chunks = split_on_silence(audio, 
                              min_silence_len=min_silence_len, 
                              silence_thresh=silence_thresh)

    # Concatenate the non-silent chunks back together
    final_audio = AudioSegment.empty()
    for chunk in chunks:
        final_audio += chunk

    # Export the result to a file
    final_audio.export(output_file, format="wav")

    print(f"Audio without silence saved to {output_file}")

