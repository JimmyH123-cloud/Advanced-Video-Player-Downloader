from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import filedialog

def download_video(url, save_path):
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Output template
            'verbose': True,  # Show detailed progress
            'concurrent_fragments': 4, # Increase concurrent downloads
            'buffer_size': 1024 * 1024, # 1 MB buffer
            'merge_output_format': 'mp4',  # Set output format for merged files
            "writesubtitles": False,
            'writeautomaticsub': False,
            # Add playlist support
            'noplaylist': True,  # Set to False to download full playlists
            # Add proxy support if needed
           
        }
        
        # Create downloader and download video
        with YoutubeDL(ydl_opts) as ydl:
            print("Starting download...")
            ydl.download([url])
            print("Download completed!")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def open_file_dialog():
    # ask path and save to variable
    folder = filedialog.askdirectory()
    # folder = "C:/Users/...
    if folder:
        print(f"Selected folder: {folder}")
    return folder

if __name__ == "__main__":
    # Create and hide the tkinter root window
    root = tk.Tk()
    root.withdraw()
    
    while True:
        
        print("\nSupported platforms include:")
        print("1. YouTube")
        print("2. Vimeo")
        print("3. Dailymotion")
        print("4. TikTok")
        print("5. Facebook")
        print("6. Instagram")
        print("7. Twitter")
        print("8. Twitch")
        print("9. Other (Any supported URL)")
        
              
        video_url = input("Please enter a YouTube URL (or 'q' to quit): ").strip()
        if video_url.lower() == 'q':
            break
            
        
        save_dir = open_file_dialog()
        
        if save_dir:
            print("Download starting...")
            download_video(video_url, save_dir)
        else:
            print("Invalid save location.")
        
        another = input("Download another video? (y/n): ").strip().lower()
        if another != 'y':
            break