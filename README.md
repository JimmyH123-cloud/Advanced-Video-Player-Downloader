# VideoToolsHub 🎥

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

A powerful suite of Python-based video tools featuring an advanced Video Playlist Player and Multi-Platform Video Downloader. Perfect for managing and downloading your video content with ease.

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
- ⏸️ **Watched Indices Loading**: press "p" to load previous watched video progress or click on file>Load Watched Video


### Video Downloader
- 🌐 **Universal Platform Support**: Download from YouTube, Vimeo, TikTok, Twitch VODs
- 📊 **Quality Optimization**: Automatic best quality selection
- ⚡ **Parallel Processing**: Faster downloads through concurrent fragments
- 🎛️ **Customizable Settings**: Configure playlists, subtitles, and proxy options

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

# Launch the application
python video_playlist_player.py
```

### Video Downloader
```bash
# Clone the repository
git clone https://github.com/jimmyH123-cloud/VideoDownloader.git

# Install dependencies
pip install yt-dlp

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
3. Select download location
4. Wait for completion

## 🐛 Known Issues
- After watching all videos, use **RTWV** (Reset Tracked Watched Videos) and press **Next** or **Play/Pause** to restart playback
- **Video Downloader** may not always download the best qualities for some videos.  

## 📄 License
This project is MIT licensed - see the [LICENSE](LICENSE) file for details

## 📬 Contact
Project Link: [https://github.com/jimmyH123-cloud/VideoToolsHub](https://github.com/jimmyH123-cloud/VideoToolsHub)
