from pydub import AudioSegment
from pydub.silence import split_on_silence

from utils import *
from pytube import YouTube

# Example usage:
input_audio = "/home/steven/Desktop/GIT/video-auto-dub/speech.acc"
output_audio = "removed_silence_audio.mp3"
remove_silence(input_audio, output_audio)

print(get_video_duration(INPUT_VIDEO_PATH))

