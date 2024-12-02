import whisper

model = whisper.load_model("turbo")
# Transcribe and translate the video file (Chinese to Spanish)
result = model.transcribe(
    "/home/steven/Desktop/GIT/video-auto-dub/videos/venom1.mp4"
)

# Store the result in a text file
with open("output_file/transcription_result.txt", "w", encoding="utf-8") as file:
    file.write(result["text"])

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