import os
import shutil
import re
from pytube import YouTube  # Import the pytube library for downloading YouTube videos
import moviepy.editor as moviepy  # Import the moviepy library for video editing
import ffmpeg  # Import the ffmpeg library for working with audio and video
import subprocess  # Import the subprocess module for running command line processes

# Function to check if a codec is available
def checkCodec(codec):
    try:
        # Run the "ffmpeg -codecs" command and capture the output
        result = subprocess.run(["ffmpeg", "-hide_banner", "-codecs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return codec in result.stdout  # Check if the codec is in the captured output
    except subprocess.CalledProcessError:
        return False

# Function to install a required codec
def installCodec(audioCodec, audioFormat):
    audioCodec = {
        'mp3': 'libmp3lame',
        'mkv': 'libvorbis',
        'mp4': 'aac',
        'm4a': 'aac',
    }.get(audioFormat, None)  # Map audio formats to their respective codecs

    if audioCodec is None:
        print(f"Unsupported audio format: {audioFormat}")
        return None

    try:
        print(f"Installing the required codec: {audioCodec}")
        cmd = f"ffmpeg -hide_banner -loglevel panic -y -c:a {audioCodec} -t 1 -f wav /dev/null"  # Install the codec
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode != 0:
            raise Exception(f"Failed to install codec: {audioCodec}")
    except Exception as e:
        print(f"An error occurred while installing the codec: {e}")

# Function to clean a filename of invalid characters and spaces
def cleanFilename(filename):
    # Remove invalid characters from the filename
    cleaned = re.sub(r'[\/:*?"<>|]', '', filename)
    
    # Replace spaces, special characters, and punctuation with underscores
    cleaned = re.sub(r'[&\s,;.!@#%^*()+=]', ' ', cleaned)
    
    return cleaned.strip()  # Remove leading/trailing spaces

# Function to download a YouTube video and save it with a sanitized filename
def downloadYoutubeVideo(videoUrl, outputDir, filename):
    try:
        os.makedirs(outputDir, exist_ok=True)  # Create the output directory if it doesn't exist
        os.chdir(outputDir)  # Change the working directory to the output directory
        yt = YouTube(videoUrl)  # Create a YouTube object with the video URL
        videoStream = yt.streams.filter(progressive=True, file_extension="mp4").first()  # Select the best video stream
        
        # Get the sanitized video title as the filename
        videoTitle = cleanFilename(yt.title)
        filename = videoTitle if not filename else cleanFilename(filename)

        videoStream.download(filename=filename + '.mp4')  # Download the video
        return f"{filename}.mp4"
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return None

# Function to convert a video to audio
def convertVideoToAudio(videoFile, audioFormat):
    try:
        if not os.path.exists(videoFile):
            raise FileNotFoundError(f"File not found: {videoFile}")
        
        clip = moviepy.VideoFileClip(videoFile)  # Create a video clip from the video file
        baseFilename, _ = os.path.splitext(os.path.basename(videoFile))  # Extract the base filename without extension
        outputFilename = f"{baseFilename}.{audioFormat}"  # Define the output audio filename
        
        audioCodec = {
            'mp3': 'libmp3lame',
            'mkv': 'libvorbis',
            'mp4': 'aac',
            'm4a': 'aac',
        }.get(audioFormat, None)  # Map audio formats to their respective codecs

        if audioCodec is None:
            print(f"Unsupported audio format: {audioFormat}")
            return None

        if not checkCodec(audioCodec):  # Check if the required codec is installed
            installCodec(audioCodec, audioFormat)  # Install the codec

        clip.audio.write_audiofile(outputFilename, codec=audioCodec)  # Convert video to audio and save it with the specified codec
        return outputFilename
    except Exception as e:
        print(f"An error occurred while converting the video to audio: {e}")
        return None

# Main function to control the workflow
def tubieConverter():
    videoUrl = input("Enter the YouTube video URL: ")
    filename = None  # Default to None to use the video title as the filename
    videoFile = downloadYoutubeVideo(videoUrl, ".", filename)  # Download the video to the "work" directory
    if videoFile:
        audioFormat = input("Enter 'mp3', 'mkv', 'mp4', or 'm4a' to save as that format: ").strip().lower()
        audioFile = convertVideoToAudio(videoFile, audioFormat)  # Convert the video to audio
        if audioFile:
            print(f"Audio saved as {audioFormat} format in {audioFile}")
