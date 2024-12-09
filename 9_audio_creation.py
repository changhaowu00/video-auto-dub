from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import time

# Your text (script)
text = [
    "Las hojas venenosas también eligieron a Eddie.",
    "Él tiene tres bocas para comer.",
    "Los buenos no comen.",
    "Los conocidos no comen.",
    "Los transeúntes no comen.",
    "En resumen,",
    "es un villano.",
    "Al mirarlo de esta manera, las hojas venenosas también causan un mal,¿verdad?"
]

# Function to create and return an audio file with the text
def create_audio_from_text(text, lang='es'):
    # Combine the text into one large string and split by sentences (use list of sentences)
    tts = gTTS(text=" ".join(text), lang=lang, slow=False)
    # Save the speech to a file
    tts.save("output.mp3")

# Create the audio file
create_audio_from_text(text)

# Load the audio file
audio = AudioSegment.from_mp3("output.mp3")

# Timing for pauses between sentences (in milliseconds)
timing = [1840, 1200, 560, 560, 800, 920, 0, 1280]  # Corresponds to each line's duration

# Create silence periods
audio_with_pauses = AudioSegment.silent(duration=0)  # Start with an empty audio

for i in range(len(text)):
    # Add the spoken audio for the current sentence
    sentence_audio = AudioSegment.from_mp3("output.mp3")[sum(timing[:i]):sum(timing[:i + 1])]
    audio_with_pauses += sentence_audio
    # Add a pause
    if i < len(timing) - 1:
        audio_with_pauses += AudioSegment.silent(duration=timing[i])

# Save the final audio with pauses
audio_with_pauses.export("final_output.mp3", format="mp3")

# Play the audio (optional)
play(audio_with_pauses)
