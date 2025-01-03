import os
import whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

from utils import add_subtitles_to_video, generate_subtitles

# Main script
video_file = os.getcwd() + "/videos/" + "venom1.mp4"
output_srt = os.getcwd() + "/output_files/" + "tts_es_subtitles.srt"
output_video = os.getcwd() + "/videos/" + "venom1_added_subtitles.mp4"
font = os.getcwd() + "/font/Roboto-BoldItalic.ttf"

# Generate subtitles and add them to the video
def parse_srt_time(srt_time):
    h, m, s = srt_time.split(":")
    s, ms = s.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

# Function to split subtitles into smaller chunks if they are too long and center-align them
def split_long_subtitles(text, max_length=40):
    words = text.split(" ")
    lines = []
    current_line = ""
    
    # Split the text into lines based on the max_length
    for word in words:
        if len(current_line + " " + word) <= max_length:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # Find the longest line length
    max_line_length = max(len(line) for line in lines)
    
    # Center-align all lines by padding with spaces on both sides
    centered_lines = []
    for line in lines:
        # Calculate spaces to pad on the left and right
        padding = (max_line_length - len(line)) // 2
        centered_line = " " * padding + line + " " * padding
        
        # In case the padding doesn't divide evenly, add an extra space to the right
        if len(centered_line) < max_line_length:
            centered_line += " "
        
        centered_lines.append(centered_line)
    
    return "\n".join(centered_lines)

def add_subtitles_to_video(video_file, srt_file, output_video, font):
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
            
            # Split long subtitles into multiple lines
            split_text = split_long_subtitles(text, max_length=40)  # Adjust max_length if necessary
           
            # Create a subtitle text clip
            subtitle_clip = TextClip(
                    text = split_text,  # Text content
                    font = font,  # Use a valid system font
                    font_size = 50,  # Font size (note: fontsize, not font_size)
                    color = "white",  # Text color
                    bg_color = "black",  # Background color for better readability
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

add_subtitles_to_video(video_file, output_srt, output_video, font)