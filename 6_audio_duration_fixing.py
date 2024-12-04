from moviepy import VideoFileClip
from pydub.utils import mediainfo
from mutagen.mp3 import MP3
import subprocess

from utils import speed_up_audio

def get_video_duration(file_path):
    # Load the video file
    video = VideoFileClip(file_path)
    
    # Get the duration of the video in seconds
    duration = video.duration
    
    # Convert the duration to minutes and seconds for better readability
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    
    return minutes, seconds

def get_mp3_duration(file_path):
    command = ['ffmpeg', '-i', file_path]
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    # Extract the duration from the stderr output
    output = result.stderr
    for line in output.splitlines():
        if "Duration" in line:
            # Extract the duration in hh:mm:ss.xx format
            duration_str = line.split('Duration: ')[1].split(',')[0]
            # Split the duration into hours, minutes, seconds, and convert everything to seconds
            h, m, s = duration_str.split(':')
            total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
            return total_seconds
    return None

# Example usage
video_file = "/home/steven/Desktop/GIT/video-auto-dub/videos/venom1.mp4"  # Replace with the path to your MP4 video
minutes, seconds = get_video_duration(video_file)
video_duration_seconds = minutes*60 + seconds
print(video_duration_seconds)

# Replace with your MP3 file path
file_path = '/home/steven/Desktop/GIT/video-auto-dub/removed_silence_audio.mp3'
duration = get_mp3_duration(file_path)
print(f"Audio Duration: {duration} seconds")

speed_up = (duration*100)/video_duration_seconds
speed_up = speed_up/100



# Example usage
input_file = "/home/steven/Desktop/GIT/video-auto-dub/speech.acc"
output_file = "adjusted_sped_up_audio.mp3"
speed_factor = speed_up # Increase the speed by 1.5x
speed_up_audio(input_file, output_file, speed_factor)