from pydub import AudioSegment
from pydub.silence import split_on_silence

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

# Example usage:
input_audio = "/home/steven/Desktop/GIT/video-auto-dub/speech.acc"
output_audio = "removed_silence_audio.mp3"
remove_silence(input_audio, output_audio)
