# VideoToolsHub

This repository contains two Python-based video tools: a Video Playlist Player and a Video Downloader.

## 1. Video Playlist Player

A Python-based video player that enables users to play videos from a folder in sequential or shuffled order, with controls for playback, volume, speed adjustment, and tracking of watched videos.

### 1.1 Features

- **Basic Playback Controls**: Play, pause, skip forward/backward, play previous/next video.
- **Playback Speed Adjustment**: Set playback speed from 0.5x to 5.0x with shortcuts.
- **Watched Videos Tracking**: Automatically skips watched videos, with a reset option.
- **Shuffle Mode**: Toggle shuffle mode for random playback order.
- **Volume Control**: Adjust volume from 0% to 125%.
- **Seek Bar and Timer**: Shows current position and allows seeking.
- **Keyboard Shortcuts**: Quick access to playback and speed controls.
- **Supported Formats**: Primarily for `.mp4` files.

### 1.2 Requirements

- Python 3.x
- `python-vlc`: `pip install python-vlc`
- VLC media player installed on your system.
- `tkinter` (usually included with Python).

### 1.3 Installation

1. Clone this repository: `git clone https://github.com/jimmyH123-cloud/VideoPlaylistPlayer.git`
2. Install dependencies: `pip install python-vlc`
3. Run: `python video_playlist_player.py`

### 1.4 Usage

1. Click **Select Folder** to choose a folder with `.mp4` videos.
2. Use buttons for play, pause, previous, and next.
3. Adjust playback speed with the slider or arrow keys.
4. Toggle **Shuffle** for random playback.
5. Use **RTWV** to reset watched videos tracking.
6. Adjust volume and seek using sliders.

### 1.5 Keyboard Shortcuts

- **Right Arrow**: Skip forward 15 seconds.
- **Left Arrow**: Skip backward 15 seconds.
- **Up Arrow**: Increase playback speed by 0.1.
- **Down Arrow**: Decrease playback speed by 0.1.

### 1.6 Possible Bugs

- If all videos in a playlist have been watched, you may need to press **RTWV** (Reset Tracked Watched Videos) and then press **Next** or **Play/Pause** to restart playback.

## 2. Video Downloader with yt-dlp

A Python script for downloading videos from various platforms like YouTube, Vimeo, TikTok, Twitch VOD (may not work in some circumstances), and others using `yt-dlp`.

### 2.1 Features

- **Multi-Platform Support**: Works with YouTube, Vimeo, TikTok, Twitch VOD, etc.
- **User-Friendly GUI**: Easy directory selection with `tkinter`.
- **High-Quality Downloads**: Best available quality selection.
- **Concurrent Downloads**: Faster downloads with increased fragments.
- **Customizable Options**: Configure playlists, subtitles, proxies.

### 2.2 Requirements

- Python 3.x
- `yt-dlp`: `pip install yt-dlp`
- `tkinter` (included with Python).

### 2.3 Installation

1. Clone this repository: `git clone https://github.com/jimmyH123-cloud/VideoDownloader.git`
2. Install dependencies: `pip install yt-dlp`
3. Run: `python video_downloader.py`

### 2.4 Usage

1. Run the script.
2. Enter the video URL from a supported platform.
3. Select the save location.
4. Wait for the download to complete.

## License

This project is licensed under the [MIT License](LICENSE).
