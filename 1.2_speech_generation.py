import openai
from pathlib import Path
from openai import OpenAI
import os
from pydub import AudioSegment
from pydub.playback import play  # Optional, for playing audio during development
import re

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def parse_srt(srt_file):
    """
    Parse an SRT file into a list of dictionaries with text and timestamps.

    Args:
        srt_file (str): Path to the SRT file.

    Returns:
        list: A list of dictionaries with 'start', 'end', and 'text'.
    """
    subtitles = []
    with open(srt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    temp_block = {}
    for line in lines:
        line = line.strip()
        if line.isdigit():
            temp_block = {}  # Start a new block
        elif "-->" in line:
            start, end = line.split(" --> ")
            temp_block["start"] = start.strip()
            temp_block["end"] = end.strip()
        elif line == "":
            if "text" in temp_block:
                subtitles.append(temp_block)
            temp_block = {}
        else:
            temp_block["text"] = temp_block.get("text", "") + " " + line.strip()
    
    if "text" in temp_block:  # Add the last block
        subtitles.append(temp_block)

    return subtitles

def srt_timestamp_to_ms(timestamp):
    """
    Convert an SRT timestamp (HH:MM:SS,ms) to milliseconds.

    Args:
        timestamp (str): Timestamp in the format "HH:MM:SS,ms".

    Returns:
        int: Time in milliseconds.
    """
    match = re.match(r"(\d+):(\d+):(\d+),(\d+)", timestamp)
    if not match:
        raise ValueError(f"Invalid timestamp format: {timestamp}")
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds

def generate_full_audio(subtitles, output_file):
    """
    Generate full TTS audio for all subtitles concatenated.

    Args:
        subtitles (list): List of subtitle dictionaries with 'text'.
        output_file (str): Path to save the full audio file.

    Returns:
        None
    """
    # Concatenate all subtitle texts
    full_text = " ".join(subtitle["text"] for subtitle in subtitles)

    # Generate TTS
    print("Generating full audio...")
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=full_text,
    )
    response.stream_to_file(output_file)

    print(f"Full audio saved: {output_file}")

def adjust_audio_to_subtitles(full_audio_path, subtitles, output_folder):
    """
    Adjust the full audio to match the duration of each subtitle.

    Args:
        full_audio_path (str): Path to the full audio file.
        subtitles (list): List of subtitle dictionaries with 'start', 'end', and 'text'.
        output_folder (str): Path to save the split audio files.

    Returns:
        None
    """
    # Load the full audio file
    print("Loading full audio...")
    full_audio = AudioSegment.from_file(full_audio_path)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for i, subtitle in enumerate(subtitles):
        start_time = srt_timestamp_to_ms(subtitle["start"])
        end_time = srt_timestamp_to_ms(subtitle["end"])

        # Extract the audio segment
        segment = full_audio[start_time:end_time]

        # Save the segment
        segment_filename = f"{output_folder}/segment_{i+1:03d}_{subtitle['start'].replace(':', '-').replace(',', '.')}_to_{subtitle['end'].replace(':', '-').replace(',', '.')}.mp3"
        segment.export(segment_filename, format="mp3")
        print(f"Saved: {segment_filename}")

    print("Audio adjustment completed!")

# Main function
def srt_to_audio_with_timing(srt_file, full_audio_file, output_folder):
    """
    Generate full audio for SRT subtitles and adjust to subtitle timings.

    Args:
        srt_file (str): Path to the SRT file.
        full_audio_file (str): Path to save the full audio file.
        output_folder (str): Path to save the split audio files.

    Returns:
        None
    """
    # Parse the SRT file
    subtitles = parse_srt(srt_file)

    # Generate the full audio
    generate_full_audio(subtitles, full_audio_file)

    # Adjust audio to match subtitle timings
    adjust_audio_to_subtitles(full_audio_file, subtitles, output_folder)

# Example Usage
srt_file_path = os.getcwd() + "/output_files/" + "tts_es_subtitles.srt"
full_audio_output_path = os.getcwd() + "output_audio/full_audio.mp3"
output_segments_folder = os.getcwd() + "output_audio/segments"

srt_to_audio_with_timing(srt_file_path, full_audio_output_path, output_segments_folder)
