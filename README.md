# VideoToolsHub 🎥

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

A powerful suite of Python-based video tools featuring an advanced Video Playlist Player and Multi-Platform Video Downloader. Perfect for managing and downloading your video content with ease.

## 🚀 Key Features

### Video Playlist Player
- 🎮 **Smart Playback Controls**: Play, pause, and navigate videos effortlessly
- ⚡ **Advanced Speed Control**: Adjust playback speed from 0.5x to 5.0x
- 🔄 **Intelligent Track Management**: Auto-skip watched videos with reset option
- 🎲 **Random Playback**: Built-in shuffle mode
- 🔊 **Enhanced Audio**: Volume control up to 125%
- ⏱️ **Progress Tracking**: Interactive seek bar with real-time timer
- ⌨️ **Keyboard Shortcuts**: Streamlined playback control

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

#### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| → | Skip forward 15s |
| ← | Skip backward 15s |
| ↑ | Increase speed 0.1x |
| ↓ | Decrease speed 0.1x |

### Video Downloader
1. Launch the application
2. Paste your video URL
3. Select download location
4. Wait for completion

## 🐛 Known Issues
- After watching all videos, use **RTWV** (Reset Tracked Watched Videos) and press **Next** or **Play/Pause** to restart playback
- After watching a video and decided to select another folder, use **RTWV** since the tracked watched video will keep track of your previous playlist to reset it and press **Next** or **Play/Pause** to restart playback  

## 📄 License
This project is MIT licensed - see the [LICENSE](LICENSE) file for details

## 📬 Contact
Project Link: [https://github.com/jimmyH123-cloud/VideoToolsHub](https://github.com/jimmyH123-cloud/VideoToolsHub)
