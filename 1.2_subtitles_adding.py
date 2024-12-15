import os
import whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

from utils import add_subtitles_to_video, generate_subtitles

# Main script
video_file = os.getcwd() + "/videos/" + "venom1.mp4"
output_srt = os.getcwd() + "/output_files/" + "tts_es_subtitles.txt"
output_video = os.getcwd() + "/videos/" + "venom1_added_subtitles.mp4"

# Generate subtitles and add them to the video
def parse_srt_time(srt_time):
    h, m, s = srt_time.split(":")
    s, ms = s.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def add_subtitles_to_video(video_file, srt_file, output_video):
    try:
        video = VideoFileClip(video_file)
        
        # Read SRT file
        with open(srt_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        subtitles = []
        for i in range(0, len(lines), 4):  # SRT blocks are typically 4 lines each
            start_time = parse_srt_time(lines[i + 1].split(" --> ")[0].strip())
            end_time = parse_srt_time(lines[i + 1].split(" --> ")[1].strip())
            text = lines[i + 2].strip()
            
            # Create a subtitle text clip
            subtitle_clip = TextClip(
                    text=text,  # Text content
                    font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Use a valid system font
                    font_size=50,  # Font size (note: fontsize, not font_size)
                    color="white",  # Text color
                    bg_color="black",  # Background color for better readability
                    size=(video.w, None),  # Match video width
                    duration = end_time - start_time
                )
            subtitle_clip.with_start(start_time)
            subtitle_clip.with_end(end_time)
            subtitle_clip.with_position(("center", "bottom"))
            subtitle_clip.start = start_time
            subtitle_clip.end = end_time


    
            subtitles.append(subtitle_clip)
        
        print(subtitles)
        # Overlay subtitles on the video
        final_video = CompositeVideoClip([video, *subtitles])
        final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")
        print(f"Video with subtitles saved to {output_video}")
    except Exception as e:
        print(f"An error occurred while adding subtitles: {e}")

add_subtitles_to_video(video_file, output_srt, output_video)