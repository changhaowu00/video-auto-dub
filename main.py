import os
import whisper

def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02}:{mins:02}:{secs:02},{millis:03}"

def generate_subtitles(video_file, output_srt, model="turbo"):
    """
    Function that generates text from speech, with the following ouput format.
        1
        00:00:00,000 --> 00:00:01,840
        outtext 
        ...
    """
    try:
        model = whisper.load_model(model)  # Use the "base" Whisper model
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

# Generate captions from video
SOURCE_VIDEO_PATH = os.getcwd() + "/videos/" +  "venom1.mp4"
WHISPER_GENERATED_TEXT_PATH = os.getcwd() + "/output_files/" +  "whisper_generated.txt"
generate_subtitles(SOURCE_VIDEO_PATH, WHISPER_GENERATED_TEXT_PATH, "turbo")

# Translate video captions


