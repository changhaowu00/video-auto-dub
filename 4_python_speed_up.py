from pydub import AudioSegment

from utils import speed_up_audio

# Example usage
input_file = "/home/steven/Desktop/GIT/video-auto-dub/speech.acc"
output_file = "sped_up_audio.mp3"
speed_factor = 1.5  # Increase the speed by 1.5x
speed_up_audio(input_file, output_file, speed_factor)
