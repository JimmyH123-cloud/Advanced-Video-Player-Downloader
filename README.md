# Advanced-Video-Player-Downloader 🎥

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

A Python toolkit for seamless video playback (VLC-powered) with preview video included and high-speed downloading from YouTube, Vimeo, and more. Features a user-friendly Tkinter GUI and customizable download options and more.

## 🚀 Key Features

### Video Playlist Player
- 🎮 **Smart Playback Controls**: Play, pause, and navigate videos effortlessly
- ⚡ **Advanced Speed Control**: Adjust playback speed from 0.5x to 4.0x
- 🔄 **Intelligent Track Management**: Auto-skip watched videos with reset option
- 🎲 **Random Playback**: Built-in shuffle mode
- 🔊 **Enhanced Audio**: Volume control up to 100%
- ⏱️ **Progress Tracking**: Interactive seek bar with real-time timer
- ⌨️ **Keyboard Shortcuts**: Streamlined playback control
- 💾 **Persistent Watched Tracking**: Saves watched video progress across sessions, handling cases where playlists change.
- 🖼️ **Video Preview**: Displays a preview thumbnail above the duration bar.
- 💬 **Merged Subtitle Support:** Load and select from multiple merged subtitle tracks.
- ⏸️ **Watched Indices Loading**: press "p" to load previous watched video progress or click on file>Load Watched Video


### Video Downloader

- 🌐 **Enhanced Platform Support**: Downloads from YouTube, Vimeo, TikTok, Twitch VODs, and more.
- 📊 **Quality Selection**: Manually choose your desired video quality.
- 🎬 **Playlist and Single Video Downloads**: Download entire playlists or individual videos as needed.
- 🎞️ **H.265/H.264 (HEVC) Support**: Supports downloading videos encoded with the H.265 codec for efficient compression or H.264 (requires ffmpeg).
- 💬 **Multiple Subtitle Downloads**: Download subtitles in multiple languages simultaneously in VTT format.
- ⚡ **Parallel Processing**: Faster downloads through concurrent fragments


## 📋 Requirements

### Video Playlist Player
```bash
# Core Requirements
python 3.x
python-vlc
VLC Media Player
tkinter (included with Python)
opencv-python
Pillow
```

### Video Downloader
```bash
# Core Requirements
python 3.x
yt-dlp
tkinter (included with Python)
ffmpeg (must be installed and accessible. Needed to be install at path: C:\)
```

## 🛠️ Installation

### Video Playlist Player
```bash
# Clone the repository
git clone https://github.com/jimmyH123-cloud/VideoPlaylistPlayer.git

# Install dependencies
pip install python-vlc
pip install opencv-python
pip install Pillow

# VLC Media Player (Required)
# Download and install VLC Media Player from [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/). Ensure you install the 64-bit version if you are using a 64-bit operating system.

# Launch the application
python video_playlist_player.py
```

### Video Downloader
```bash
# Clone the repository
git clone https://github.com/jimmyH123-cloud/VideoDownloader.git

# Install dependencies
pip install yt-dlp

## Install External Dependencies
# ffmpeg (Required for H.265/HEVC / H.264/AVC)
# This is essential. Follow these steps:

# 1. Download ffmpeg:
#    * Go to [https://www.gyan.dev/ffmpeg/builds/] or [https://www.ffmpeg.org/download.html] and find the gyan.dev build.
#    * Look for the latest "Essentials" or "Release" builds. Choose the correct version for your operating system (Windows 64-bit is most common). It will be a .zip file.
#    * Download the .zip or 7z file.

# 2. Extract ffmpeg:
#    * Extract the *contents* of the downloaded .zip file directly in your C: drive (C:\ffmpeg). This is the recommended location for simplicity.
#    * Rename the folder ffmpeg-..-.. to ffmpeg.
#    * You should now have a folder structure like C:\ffmpeg\bin, C:\ffmpeg\doc, etc. 
# And if it doesn't print "... - ERROR - FFmpeg not found at C:\ffmpeg\bin\ffmpeg.exe" after launching the script then it should work


# Launch the application
python video_downloader.py
```

## 📖 Usage Guide

### Video Playlist Player
1. Launch the application and click **Select Folder**
2. Choose a directory containing `.mp4` files
3. Use the intuitive controls for playback
4. Adjust speed using slider or keyboard shortcuts
5. Toggle shuffle mode for random playback
6. Reset watched videos with **RTWV** button
7.  **Persistent Watched Video Tracking:**
    *   Pressing `<p>` will save the currently tracked watched videos to a file (`watched_videos.txt`) in the same directory as the script. This allows you to resume your progress in future sessions.
    *   Pausing the video will *not* automatically save the watched videos. You must use the `<p>` key or the "Save Watched Videos" menu option to save your progress.
    *   When the application starts, you can choose to load previously tracked videos using the "Load Watched Videos" menu option.
    *   **Handling Different Playlists:** If you load watched video data from a previous session and some of the tracked videos are *not* present in the current playlist, a warning message will be displayed, and those invalid entries will be ignored. Only the valid entries for the current playlist will be loaded.
8. **Merged Subtitle Support:** If your videos have merged subtitles (e.g., embedded within the video file), the player will detect them and allow you to select which track to display. You can select them from the menu option


#### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| → | Skip forward 15s |
| ← | Skip backward 15s |
| ↑ | Increase speed 0.1x |
| ↓ | Decrease speed 0.1x |
| p   | Save watched video tracking to `watched_videos.txt` |

### Video Downloader
1. Launch the application
2. Paste your video URL
3. Select the output directory.
4. Select Video Quality: Choose your desired video quality.
5. Wait for completions
6. (Playlist option) Repeat step 4 and 5. 

## 🐛 Known Issues
- After watching all videos, use **RTWV** (Reset Tracked Watched Videos) and press **Next** or **Play/Pause** to restart playback
- **Video Downloader:** The downloading proccessing may take severals minutes depending on the file size, `resolution` (1080p, 4K), `codec` used to convert, `subtitle merging` and `internet speed`. (If the terminal is freezing for a while, it mean that it's proccessing. )
 

## 📄 License
This project is MIT licensed - see the [LICENSE](LICENSE) file for details

## 📬 Contact
Project Link: [https://github.com/jimmyH123-cloud/VideoToolsHub](https://github.com/jimmyH123-cloud/VideoToolsHub)
