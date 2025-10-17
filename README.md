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
ffmpeg (must be installed and accessible)
```

## 🛠️ Installation

**First, clone the repository:**
```bash
git clone [https://github.com/JimmyH123-cloud/Advanced-Video-Player-Downloader.git](https://github.com/JimmyH123-cloud/Advanced-Video-Player-Downloader.git)
cd Advanced-Video-Player-Downloader
```

### Video Playlist Player
```bash

# Install dependencies
pip install python-vlc
pip install opencv-python
pip install Pillow

# VLC Media Player (Required)
```

#### Platform-Specific VLC Installation (Required)
**Windows:** Download and install the 64-bit version from https://www.videolan.org/vlc/.

**Linux (Debian/Ubuntu):** Install both the player and the library headers:

```bash
sudo apt update
sudo apt install vlc libvlc-dev
```
**macOS:** Install via Homebrew:

```bash
brew install vlc
```

### Video Downloader

```bash
# Install dependencies
pip install yt-dlp
```


#### ⚙️ FFmpeg Installation (Required for Video Conversion and Subtitles)

`ffmpeg` is mandatory for video conversion (H.265/H.264) and subtitle embedding. The program automatically detects it if it’s available in your system **PATH** or through the environment variable `FFMPEG_PATH`.

##### Option 1 – Recommended (Install via Package Manager or Add to PATH)

1.  **Installation Commands:**

      * **Windows:**
        1.  Download the build from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/).
        2.  Extract the archive (e.g., to `C:\ffmpeg`). Ensure `ffmpeg.exe` is in the `C:\ffmpeg\bin` directory.
        3.  **Add `C:\ffmpeg\bin` to your System PATH** Environment Variables (Press `Win + R`, type `sysdm.cpl`, go to **Advanced → Environment Variables**).
      * **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt install ffmpeg
        ```
      * **macOS (Homebrew):**
        ```bash
        brew install ffmpeg
        ```
      

2.  **Verify Installation:**
    Open a **new** terminal window and run:

    ```bash
    ffmpeg -version
    ```

    If this prints version info, it’s correctly configured.

##### Option 2 – Environment Variable (Custom Location)

If you cannot modify the system PATH or does not want to, you can set the `FFMPEG_PATH` environment variable to the exact location of the executable.

```bash
# Windows PowerShell
setx FFMPEG_PATH "C:\custom\path\to\ffmpeg.exe"

# Linux/macOS (add to your shell profile, e.g., .bashrc, .zshrc)
export FFMPEG_PATH="/usr/local/bin/ffmpeg"
```

The application will automatically detect this custom path.


## 📖 Usage Guide

### Video Playlist Player

<details>

<summary>Usage of Video Playlist Player</summary>

1. Launch the application using the appropriate script for your OS:
   ```bash 
   # For Windows
   python video_playlist_player.py

   # For Linux / macOS (Includes logic for platform-specific video frame handling) and (WSL Excluded)
   python video_playlist_player_linux_mac.py
   ```
2. and click **Select Folder**
3. Choose a directory containing `.mp4` files
4. Use the intuitive controls for playback
5. Adjust speed using slider or keyboard shortcuts
6. Toggle shuffle mode for random playback
7. Reset watched videos with **RTWV** button
8.  **Persistent Watched Video Tracking:**
    *   Pressing `<p>` will save the currently tracked watched videos to a file (`watched_videos.txt`) in the same directory as the script. This allows you to resume your progress in future sessions.
    *   Pausing the video will *not* automatically save the watched videos. You must use the `<p>` key or the "Save Watched Videos" menu option to save your progress.
    *   When the application starts, you can choose to load previously tracked videos using the "Load Watched Videos" menu option.
    *   **Handling Different Playlists:** If you load watched video data from a previous session and some of the tracked videos are *not* present in the current playlist, a warning message will be displayed, and those invalid entries will be ignored. Only the valid entries for the current playlist will be loaded.
9.  **Merged Subtitle Support:** If your videos have merged subtitles (e.g., embedded within the video file), the player will detect them and allow you to select which track to display. You can select them from the menu option

</details>

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
   ```bash
   # Window, Linux Or MacOS
   python video_downloader.py
   ```
2. Paste your video URL
3. Select the output directory.
4. Select Video Quality: Choose your desired video quality.
5. Wait for completions
6. (Playlist option) Repeat step 4 and 5. 

#### Settings
```py
# Defaults

# Controls whether subtitle files leftover after embedding are kept.
GET_SUBTITLE_LEFTOVER = False  # Set True/False

# Optional cookies file (not required by default).
# Use only if you hit anti-bot detection; contains session tokens.
# COOKIES_NAME = 'cookies.txt'  # Uncomment to enable

# Controls whether the downloader requests subtitles via yt-dlp.
# If True, yt-dlp will attempt to download subtitles (may trigger HTTP 429).
DOWNLOAD_SUBTITLES = True      # Set True/False
```

#### Quick 429 troubleshooting

> refer to https://github.com/yt-dlp/yt-dlp/issues/13831
- If you get HTTP 429 for subtitles, set DOWNLOAD_SUBTITLES = False to download video only. or check if the specific video has the specific subtitle available


## 🐛 Known Issues
- After watching all videos, use **RTWV** (Reset Tracked Watched Videos) and press **Next** or **Play/Pause** to restart playback
- **Video Downloader:** The downloading processing may take severals minutes depending on the file size, `resolution` (1080p, 4K), `codec` used to convert, `subtitle merging` and `internet speed`. (If the terminal is freezing for a while, it mean that it's processing. )
 

## 📄 License
This project is MIT licensed - see the [LICENSE](LICENSE) file for details

## 📬 Contact
Project Link: [https://github.com/jimmyH123-cloud/VideoToolsHub](https://github.com/jimmyH123-cloud/VideoToolsHub)

