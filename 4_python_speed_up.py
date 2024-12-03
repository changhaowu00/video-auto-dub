from pydub import AudioSegment

def speed_up_audio(input_file, output_file, speed_factor=1.5):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Speed up the audio by changing the playback speed
    # Speed factor > 1 will speed up, < 1 will slow down
    sped_up_audio = audio.speedup(playback_speed=speed_factor)

    # Export the sped-up audio to a new file
    sped_up_audio.export(output_file, format="mp3")

    print(f"Audio saved as {output_file}")

# Example usage
input_file = "/home/steven/Desktop/GIT/video-auto-dub/speech.acc"
output_file = "sped_up_audio.mp3"
speed_factor = 1.5  # Increase the speed by 1.5x
speed_up_audio(input_file, output_file, speed_factor)
