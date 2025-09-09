import tkinter as tk
from tkinter import filedialog
from yt_dlp import YoutubeDL
import os
import glob
import logging
from collections import defaultdict
import subprocess
import time
# from yt_dlp.networking.impersonate import ImpersonateTarget

# basic log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VideoDownloader:
    # SETTINGS, can be configure freely
    
    GET_SUBTITLE_LEFTOVER = False # Set True/False | Option to keep the subtitle as file, if the user want to modify the subtitle or use it later.
    
    # COOKIES_NAME = 'cookies.txt' # Not needed until issues appear. Option to use youtube_cookies in case if yt anti bot detect.
    
    DOWNLOAD_SUBTITLES = True # Set True/False | Option to download the subtitle, if True, cautious as HTTP Error 429 might happen with Youtube if the specific subtitle is not available in the video
    
    
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg.exe' # You need to install ffmpeg at C: otherwise it won't found the ffmpeg
        
        # Verify FFmpeg installation
        if not os.path.exists(self.ffmpeg_path):
            logging.error(f"FFmpeg not found at {self.ffmpeg_path}")
            self.ffmpeg_path = filedialog.askopenfilename(title="Locate ffmpeg.exe")
            if not os.path.exists(self.ffmpeg_path):
                logging.error("FFmpeg is still not found. Exiting.")
                exit(1)
        else:
            logging.info(f"Found FFmpeg at: {self.ffmpeg_path}")

    # Print download progress.
    def print_progress(self, d):
        
        if d['status'] == 'downloading':
            try:
                if 'total_bytes' in d:
                    percentage = d['downloaded_bytes'] / d['total_bytes'] * 100
                    downloaded_mb = d['downloaded_bytes'] / 1024 / 1024
                    total_mb = d['total_bytes'] / 1024 / 1024
                    print(f"\rProgress: {percentage:.1f}% ({downloaded_mb:.1f}MB of {total_mb:.1f}MB)", end='')
                elif 'downloaded_bytes' in d:
                    downloaded_mb = d['downloaded_bytes'] / 1024 / 1024
                    print(f"\rDownloaded: {downloaded_mb:.1f}MB", end='')
            except:
                print(f"\rDownloading...", end='')
        elif d['status'] == 'finished':
            print("\nDownload completed!")

    # Get available video formats.
    def get_video_formats(self, url):
        
        ydl_opts = {
            'ffmpeg_location': self.ffmpeg_path,
            'quiet': False,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Group formats by resolution
            formats_by_res = defaultdict(list)
            video_formats = []
            
            for f in info['formats']:
                # Skip audio-only formats
                if f.get('vcodec') == 'none': 
                    continue
                    
                # Get resolution
                res = f.get('resolution', 'unknown')
                height = f.get('height', 0)
                
                # Create format info
                format_info = {
                    'format_id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': res,
                    'filesize': f.get('filesize', 0),
                    'vcodec': f.get('vcodec', 'unknown'),
                    'acodec': f.get('acodec', 'unknown'),
                    'height': height,
                }
                
                formats_by_res[height].append(format_info)
                video_formats.append(format_info)
            
            return info, formats_by_res, video_formats

    # Returns the base ydl options for all requests to avoid rate limiting
    def get_base_ydl_opts(self):
        return {
            'socket_timeout': 15,
            # 'retries': 10, # not needed until issues appear
            # 'fragment_retries': 10,
            # 'sleep_interval': 2, 
            # 'max_sleep_interval': 6,
            # 'sleep_subtitles': 5, 
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
        }
    
    # Extract video URLs from a playlist.
    def get_playlist_videos(self, url):
        
        ydl_opts = self.get_base_ydl_opts()
        ydl_opts['extract_flat'] = 'in_playlist'
        ydl_opts['quiet'] = True
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                # Extract video URLs from playlist
                logging.info(f"Found {len(info['entries'])} videos in the playlist.")
                video_urls = {entry['url'] for entry in info['entries']}
                return video_urls
            else:
                logging.error("Not a valid playlist URL or no videos found.")
                return set()

    # Display available video formats.
    def display_formats(self, formats_by_res):
        
        print("\nAvailable video qualities:")
        print("0. Best quality (automatic)")
        
        # Sort resolutions in descending order
        sorted_heights = sorted(formats_by_res.keys(), reverse=True)
        
        for idx, height in enumerate(sorted_heights, 1):
            formats = formats_by_res[height]
            if height == 0:
                continue
                
            # Get filesize of the first format in this resolution
            size_mb = formats[0]['filesize'] / (1024 * 1024) if formats[0]['filesize'] > 0 else 0
            size_str = f"{size_mb:.1f}MB" if size_mb > 0 else "Unknown size"
            
            print(f"{idx}. {height}p ({size_str})")
        print(f"{idx + 1}. Cancelled the video")
        return sorted_heights

    # Verify if the downloaded file is complete.
    def verify_file_integrity(self, file_path, expected_size):
        
        if os.path.exists(file_path):
            actual_size = os.path.getsize(file_path)
            return actual_size == expected_size
        return False
    
    
    # Replace invalid characters in case if file name is invalid
    def sanitize_filename(self, filename):
        
        invalid_chars = '<>:"/\\|?*[]'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def reencode_video(self, input_path, output_path, subtitle_paths=None):
        try:    
            logging.info(f"Re-encoding video: {input_path} -> {output_path}")
            if subtitle_paths:
                logging.info(f"Subtitles to merge: {subtitle_paths}")
            
            command = [
                self.ffmpeg_path,
                '-i', input_path,  # Input video file
            ]

            # Add subtitle inputs if available
            if subtitle_paths:
                for sub_path in subtitle_paths:
                    command.extend(['-i', sub_path])

            command.extend([
                '-c:v', 'copy',  # Copy video stream (no re-encoding)
                '-c:a', 'copy',  # Copy audio stream (no re-encoding)
                '-map', '0:v',   # Map video stream from input 0
                '-map', '0:a',   # Map audio stream from input 0
                '-threads', '2',  # Limit threads to reduce CPU load
                '-preset', 'medium ',  # Use the (x) preset
                '-map_metadata', '-1',  # Skip writing metadata: title,creation_date,etc..
            ])

            # Map subtitles if available
            if subtitle_paths:
                for idx, sub_path in enumerate(subtitle_paths, start=1):
                    command.extend([
                        '-map', f'{idx}:s',  # Map subtitle stream from input idx
                        f'-metadata:s:s:{idx-1}', f'language={sub_path[-6:-4]}',  # Set subtitle language
                        f'-metadata:s:s:{idx-1}', f'title=subtitle.{sub_path[-6:-4]}',  # Set subtitle track title
                    ])
                command.extend(['-c:s', 'mov_text'])  # Embed subtitles as mov_text format

            command.append(output_path)  # Output file
            
            
            logging.info(f"Running FFmpeg command: {' '.join(command)}")

            # Run the command and capture output
            _ = subprocess.run(
                command, 
                stdout=subprocess.DEVNULL,  # Discard stdout
                stderr=subprocess.DEVNULL,  # Discard stderr
                text=True, 
                encoding="utf-8", 
                errors='replace', 
                check=True
            )
            
            logging.info("Re-encoding completed successfully.")
            return True

        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg re-encoding failed: {str(e)}")
            logging.error(f"FFmpeg output:\n{e.stdout}")
            logging.error(f"FFmpeg errors:\n{e.stderr}")
            return False

    
    # Download a video with optional re-encoding and subtitle embedding.
    def download_video(self, url, save_path, selected_height=None):
        
        try:
            # Get video information and available formats
            info, formats_by_res, video_formats = self.get_video_formats(url)
            sorted_heights = self.display_formats(formats_by_res)

            # Let user choose quality
            while True:
                choice = input("\nSelect quality (number): ").strip()
                try:
                    choice_idx = int(choice)
                    if choice_idx == 0:
                        # Best quality (automatic): Try HEVC first,then AVC, then fallback
                        format_code = (
                            'bestvideo[ext=mp4][vcodec^=hevc]+bestaudio[ext=m4a]/'  # HEVC (H.265) format: 313 
                            'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/'  # AVC (H.264) format: 137 or 299
                            'bestvideo[ext=mp4]+bestaudio[ext=m4a]/'                # Any MP4 video VP9 format: 298
                            'bestvideo+bestaudio/best'                              # Fallback to best available
                        )
                        break
                    elif 1 <= choice_idx <= len(sorted_heights):
                        
                        # Specific resolution: Try HEVC first, then AVC, then fallback
                        selected_height = sorted_heights[choice_idx - 1]
                        format_code = (
                            f'bestvideo[height<={selected_height}][ext=mp4][vcodec^=hevc]+bestaudio[ext=m4a]/'  # HEVC (H.265) format: 313
                            f'bestvideo[height<={selected_height}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/'  # AVC (H.264) format: 137 or 299
                            f'bestvideo[height<={selected_height}][ext=mp4]+bestaudio[ext=m4a]/'                # Any MP4 video VP9 format: 298
                            f'bestvideo[height<={selected_height}]+bestaudio/best'                              # Fallback to best available
                        )
                        break
                    elif choice_idx == len(sorted_heights) + 1:
                        return False  # Cancelled
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            video_title = info.get('title', 'video')
            sanitized_title = self.sanitize_filename(video_title)
            
            
            # Configure ydl_opts
            ydl_opts = self.get_base_ydl_opts() # add base configuration
            ydl_opts.update({
                # 'cookiefile': self.COOKIES_NAME, # not needed until issues appear
                # 'impersonate': ImpersonateTarget('chrome'),  not needed until issues appear
                'format': format_code,
                'outtmpl': os.path.join(save_path, f"{sanitized_title}.%(ext)s"),
                'merge_output_format': 'mp4',
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [self.print_progress],
                'concurrent_fragment_downloads': 2,  # Enable multithreaded downloads to make the downloading faster. Be cautious of server limit if increasing fragments
            })
            
            if self.DOWNLOAD_SUBTITLES: 
                ydl_opts.update({
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitlesformat': 'ass',
                    'subtitleslangs': ['en'],  # Download subtitles. If you want to download a specific subtitle, just add to the list. For example: ["en", "fr", "es", "ja", "cn"] 
                    'postprocessors': [
                        {
                            'key': 'FFmpegSubtitlesConvertor',
                            'format': 'ass',
                        },
                    ],
                })
                

            # Download video and subtitles
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                logging.error(f"\nError downloading the video: {str(e)}")
                return False

            # Verify file integrity
            video_file = os.path.join(save_path, f"{sanitized_title}.mp4")            
            if not os.path.exists(video_file):
                logging.error("Downloaded file not found.")
                return False
            
            if self.DOWNLOAD_SUBTITLES:
                # Get subtitle paths
                subtitle_files = glob.glob(os.path.join(save_path, f"{glob.escape(sanitized_title)}.*.ass"))
                logging.info(f"Subtitles found: {subtitle_files}")
            else:
                subtitle_files = None
            
            # Re-encode video and embed subtitles
            temp_output_file = os.path.join(save_path, f"{sanitized_title}_with_subs.mp4")
            if not self.reencode_video(video_file, temp_output_file, subtitle_files):
                logging.error("Failed to re-encode video with subtitles.")
                return False
        
            time.sleep(1) # give some time to process (optional can be removed if not created issues)
            
            # Check if the re-encoded file exists
            if not os.path.exists(temp_output_file):
                logging.error(f"Re-encoded file not found: {temp_output_file}")
                return False
            
            # Replace the original video with the new one
            os.remove(video_file)
            final_output_file = os.path.join(save_path, f"{video_title}.mp4")
            
            if self.DOWNLOAD_SUBTITLES and not self.GET_SUBTITLE_LEFTOVER:
                # Clean up leftover subtitle files
                for sub_file in subtitle_files:
                    if os.path.exists(sub_file):
                        os.remove(sub_file)
                        logging.info(f"Deleted leftover subtitle file: {sub_file}")
            
            # Attempt to keep the original name (sometime won't work due to Window special character restriction)
            try:
                os.rename(temp_output_file, final_output_file)
                print(f"'{os.path.basename(temp_output_file)}' was rename to '{os.path.basename(final_output_file)}'")
            except WindowsError as e:
                logging.error(f"Error renaming video title.")
            
            return True

        except Exception as e:
            logging.error(f"\nError downloading video: {str(e)}")
            return False

    # If downloading failed, attempt to delete any left over
    def cleanup_subtitles(self, save_dir, video_title):
        try:
            subtitle_files = glob.glob(os.path.join(save_dir, f"{video_title}.*.ass"))
            for file in subtitle_files:
                if os.path.exists(file):
                    os.remove(file)
                    logging.info(f"Deleted leftover subtitle file: {file}")
        except Exception as e:
            logging.error(f"Error deleting leftover subtitle files: {str(e)}")

    def run(self):
        "Main loop for downloading videos."
        while True:
            try:
                video_url = input("\nEnter video or playlist URL (or 'q' to quit): ").strip()
                if video_url.lower() == 'q':
                    break
                
                save_dir = filedialog.askdirectory(title="Select Download Location")
                if not save_dir:
                    logging.error("Error: No directory selected")
                    continue
                
                if 'list=' in video_url:  # Check if the URL contains a playlist identifier
                    logging.info("\nDetected a playlist URL. Extracting video links...")
                    video_urls = self.get_playlist_videos(video_url)
                    if not video_urls:
                        logging.error("No videos found in the playlist.")
                        continue
                    
                    logging.info(f"Found {len(video_urls)} videos in the playlist.")
                    
                    # Get a set of already downloaded videos (by filename)
                    downloaded_files = {f for f in os.listdir(save_dir) if f.endswith('.mp4')}
                    
                    for idx, url in enumerate(video_urls, 1):
                        # Extract the video title (used as filename)
                        ydl_opts = {
                            'quiet': True,
                            'ffmpeg_location': self.ffmpeg_path,
                        }
                        
                        with YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            video_title = info.get('title', 'Unknown')
                            filename = f"{video_title}.mp4"
                            
                        if filename in downloaded_files:
                            logging.info(f"\nVideo '{video_title}' already downloaded. Skipping...")
                            continue
                        
                        logging.info(f"\nDownloading video {idx}/{len(video_urls)}: {video_title}")
                        success = self.download_video(url, save_dir)
                        
                        if self.DOWNLOAD_SUBTITLES and not success:
                            self.cleanup_subtitles(save_dir, video_title)
                            logging.error(f"Failed to download video {idx}. Continuing with the next one...")  
                else:
                    # Single video download
                    success = self.download_video(video_url, save_dir)
                    if self.DOWNLOAD_SUBTITLES and not success:
                        with YoutubeDL({'quiet': True}) as ydl:
                            info = ydl.extract_info(video_url, download=False)
                            video_title = info.get('title', 'Unknown')
                        self.cleanup_subtitles(save_dir, video_title)
                
                another = input("\nDownload another video or playlist? (y/n): ").strip().lower()
                if another != 'y':
                    break
            except KeyboardInterrupt:
                logging.info("\nProgram interrupted by user.")
                break
            except Exception as e:
                logging.error(f"\nAn unexpected error occurred: {str(e)}")
                continue

if __name__ == "__main__":
    try:
        downloader = VideoDownloader()
        downloader.run()
    except Exception as e:
        logging.error(f"\nFatal error: {str(e)}")
        exit(1)

