import os
import whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

from utils import add_subtitles_to_video, generate_subtitles

# Main script
video_file = 's2s.mp4'  
output_srt = "output_subtitles.srt"
output_video = "output_video_with_subtitles.mp4"

# Generate subtitles and add them to the video
add_subtitles_to_video(video_file, output_srt, output_video)
