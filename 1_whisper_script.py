import os
import whisper
from utils import *

# Transcribe and translate the video file (Chinese to Spanish)
model = whisper.load_model("turbo")
generate_subtitles(INPUT_VIDEO_PATH, OUTPUT_TEXT_PATH, model)

