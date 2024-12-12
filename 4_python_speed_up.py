from utils import *

# Example usage
input_file = os.getcwd() +"/speech.acc"
output_file = "sped_up_audio.mp3"
speed_factor = 1.5  # Increase the speed by 1.5x
speed_up_audio(input_file, output_file, speed_factor)
