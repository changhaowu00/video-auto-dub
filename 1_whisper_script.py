import os
import whisper
from utils import *

# Transcribe and translate the video file (Chinese to Spanish)
model = whisper.load_model("turbo")
result = model.transcribe(INPUT_VIDEO_PATH)

# Store the result in a text file
with open(OUTPUT_TEXT_PATH, "w", encoding="utf-8") as file:
    file.write(result["text"])

generate_subtitles(INPUT_VIDEO_PATH, OUTPUT_TEXT_PATH)
# model = whisper.load_model("turbo")

# # load audio and pad/trim it to fit 30 seconds
# audio = whisper.load_audio("C:\\Users\\chang\\Downloads\\output_audio.mp3")
# audio = whisper.pad_or_trim(audio)

# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)

# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")

# # decode the audio
# options = whisper.DecodingOptions()
# result = whisper.decode(model, mel, options)

# # print the recognized text
# print(result.text)