# File config
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import whisper
from moviepy import * 

FILENAME = "venom1"
INPUT_VIDEO_PATH = os.getcwd() + "/videos/" + FILENAME + ".mp4"
OUTPUT_TEXT_PATH = os.getcwd() + "/output_files/" + FILENAME + ".txt"

def speed_up_audio(input_file, output_file, speed_factor=1.5):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Speed up the audio by changing the playback speed
    # Speed factor > 1 will speed up, < 1 will slow down
    sped_up_audio = audio.speedup(playback_speed=speed_factor)

    # Export the sped-up audio to a new file
    sped_up_audio.export(output_file, format="mp3")

    print(f"Audio saved as {output_file}")

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

# Helper function to parse SRT time
def parse_srt_time(srt_time):
    h, m, s = srt_time.split(":")
    s, ms = s.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
