from moviepy import VideoFileClip, AudioFileClip
from moviepy.editor import * 

def replace_audio_in_video(video_file, audio_file, output_file):
    # Load the video clip
    video_clip = VideoFileClip(video_file)
    
    # Load the audio file (MP3)
    audio_clip = AudioFileClip(audio_file)
    
    # Set the new audio for the video
    video_clip = video_clip.with_audio(audio_clip)
    
    # Write the result to a new file
    video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

def combine_audio(vidname, audname, outname, fps=60): 

    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)

# Replace with your file paths
video_file = '/home/steven/Desktop/GIT/video-auto-dub/videos/venom1.mp4'       # Your MP4 video file
audio_file = '/home/steven/Desktop/GIT/video-auto-dub/adjusted_sped_up_audio.mp3'  # Your MP3 file to replace the audio
output_file = 'ssss.mp4'     # The name of the output file

replace_audio_in_video(video_file, audio_file, output_file)

print(f"Audio in {video_file} has been replaced with {audio_file}. Output saved as {output_file}.")
