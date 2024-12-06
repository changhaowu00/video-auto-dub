import os
import whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

# Function to generate subtitles using Whisper
def generate_subtitles(video_file, output_srt):
    try:
        model = whisper.load_model("base")  # Use the "base" Whisper model
        result = model.transcribe(video_file)
        
        # Save subtitles in SRT format
        with open(output_srt, "w") as f:
            for i, segment in enumerate(result["segments"]):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                
                f.write(f"{i + 1}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")
                
        print(f"Subtitles saved to {output_srt}")
    except Exception as e:
        print(f"An error occurred while generating subtitles: {e}")

# Helper function to format time in SRT format
def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02}:{mins:02}:{secs:02},{millis:03}"

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
                    font_size=24,  # Font size (note: fontsize, not font_size)
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
            subtitle_clip.pos = ("center", "bottom")


    
            subtitles.append(subtitle_clip)
        
        # Overlay subtitles on the video
        final_video = CompositeVideoClip([video, *subtitles])
        final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")
        print(f"Video with subtitles saved to {output_video}")
    except Exception as e:
        print(f"An error occurred while adding subtitles: {e}")


# Helper function to parse SRT time
def parse_srt_time(srt_time):
    h, m, s = srt_time.split(":")
    s, ms = s.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

# Main script
video_file = 's2s.mp4'  
output_srt = "output_subtitles.srt"
output_video = "output_video_with_subtitles.mp4"

# Generate subtitles and add them to the video
generate_subtitles(video_file, output_srt)
add_subtitles_to_video(video_file, output_srt, output_video)
