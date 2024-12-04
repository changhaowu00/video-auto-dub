def get_video_duration(file_path):
    # Load the video file
    video = VideoFileClip(file_path)
    
    # Get the duration of the video in seconds
    duration = video.duration
    
    # Convert the duration to minutes and seconds for better readability
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    
    return minutes, seconds

# Example usage
video_file = "your_video.mp4"  # Replace with the path to your MP4 video
minutes, seconds = get_video_duration(video_file)
print(f"The video duration is {minutes} minutes and {seconds} seconds.")