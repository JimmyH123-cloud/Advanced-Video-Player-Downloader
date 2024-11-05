import tkinter as tk
from tkinter import ttk, filedialog
import os
import vlc
import random
from pathlib import Path


class VideoPlayer:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Video Playlist Player")
        self.root.geometry("900x650")
        
        # Initialize VLC instance and media player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        # Initialize playlist attributes
        self.playlist = []  # List to store video file paths
        self.current_index = 0  # Index of the current video in playlist
        self.is_playing = False  # Flag to track play/pause state
        self.is_shuffle = False  # Flag to enable/disable shuffle mode
        self.playback_speed = 1.0 # Default playback Speed
        
        # keep tracked of watched videos
        self.watched_videos = set()
        

        # Setup the user interface
        self.setup_ui()
        
        # Bind keys
        self.bind_keys()
        
    def setup_ui(self):
        # Create main container frame
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=7, pady=4)
        
        # Create video display frame
        self.video_frame = ttk.Frame(main_container, borderwidth=2, relief='solid')
        self.video_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # Set the desired aspect ratio for the video
        self.video_frame.bind("<Configure>", self.on_frame_resize)
        
        # add a bar to move the duration of the video
        self.duration_var = tk.DoubleVar()
        self.duration_slider = ttk.Scale(
            main_container, from_=0, to=100, orient=tk.HORIZONTAL,
            variable=self.duration_var, command=self.on_duration_change
        )
        self.duration_slider.pack(fill=tk.X, padx=5, pady=5)

        
        # Timer label
        self.timer_label = ttk.Label(main_container, text="00:00 / 00:00")
        self.timer_label.pack(pady=5)

        
        # Create control button frame
        controls = ttk.Frame(main_container)
        controls.pack(fill=tk.X, pady=4)

        
        # Control buttons
        ttk.Button(controls, text="Select Folder", command=self.load_folder).pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Previous", command=self.play_previous, width=7.5).pack(side=tk.LEFT, padx=2,pady=2)
        self.play_button = ttk.Button(controls, text="Play", command=self.toggle_play, width=5)
        self.play_button.pack(side=tk.LEFT, padx=2,pady=2)
        ttk.Button(controls, text="Next", command=self.play_next, width=5).pack(side=tk.LEFT, padx=2,pady=2)


        # Skip buttons
        ttk.Button(controls, text="Skip Back 15s", command=self.skip_back).pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Skip Forward 15s", command=self.skip_forward).pack(side=tk.LEFT, padx=4)

        
        # "RTWV" initial for Reset Traked Watched Videos
        # you can change the initial if you want
        ttk.Button(controls, text="RTWV", command=self.reset_watched_videos, width=6.5).pack(side=tk.LEFT, padx=2,pady=2)


        # Shuffle toggle button
        self.shuffle_button = ttk.Button(controls, text="Shuffle On", command=self.toggle_shuffle)
        self.shuffle_button.pack(side=tk.LEFT, padx=4)
        
        # Volume control slider
        self.volume_var = tk.IntVar(value=100)
        volume_slider = ttk.Scale(controls, from_=0, to=125, orient=tk.HORIZONTAL,
                                  variable=self.volume_var, command=self.set_volume)
        volume_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Playlist display frame
        playlist_frame = ttk.Frame(main_container)
        playlist_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Playlist listbox to show videos
        self.playlist_box = tk.Listbox(playlist_frame, selectmode=tk.SINGLE)
        self.playlist_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar for playlist
        scrollbar = ttk.Scrollbar(playlist_frame, orient=tk.VERTICAL, 
                                  command=self.playlist_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist_box.config(yscrollcommand=scrollbar.set)
        
        # Set the Décélération/accéleration
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_slider = ttk.Scale(controls, from_=0.5, to=2.0, orient=tk.HORIZONTAL,
                        variable=self.speed_var, command=self.set_speed)
        speed_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Add a label to display the current speed 
        self.speed_label = ttk.Label(controls, text="Speed: 1.0x")
        self.speed_label.pack(side=tk.LEFT)
        
        # Bind double-click on playlist items to play the selected video
        self.playlist_box.bind('<Double-Button-1>', self.play_selected)
        
        # Bind close window event to stop playback
        # Remove the container if <exit> is used
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_folder(self):
        # Open folder selection dialog
        folder = filedialog.askdirectory()
        if folder:
            # Clear current playlist and listbox
            self.playlist.clear()
            self.playlist_box.delete(0, tk.END)
            
            # Load all MP4 files from the selected folder
            for file in Path(folder).glob("*.mp4"):
                self.playlist.append(str(file))
                self.playlist_box.insert(tk.END, file.name)
            
            # Start playing the first video in the playlist if any
            if self.playlist:
                self.toggle_shuffle()
                self.reset_watched_videos()
                self.current_index = 0
                self.play_current()
    
    def play_current(self):
        # Play the video at the current index in the playlist
        if 0 <= self.current_index < len(self.playlist):
            media = self.instance.media_new(self.playlist[self.current_index])
            self.player.set_media(media)
            
            # Set the window ID to render VLC's video output
            if os.name == 'nt':  # Windows
                self.player.set_hwnd(self.video_frame.winfo_id())
            else:  # Set Linux/Mac ID to render VLC's video output
                self.player.set_xwindow(self.video_frame.winfo_id())
            
            # Start playback
            self.player.play()
            self.is_playing = True
            self.play_button.config(text="Pause")
            
            # Highlight the currently playing video in the playlist
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(self.current_index)
            self.playlist_box.see(self.current_index)
            
            # Mark the current video as watched
            self.watched_videos.add(self.current_index)
            
            # Set up end-of-video check to play the next video
            self.update_duration_slider()
    
    def check_end(self):
        # Check if the video has ended and play the next one if it has
        if self.player.get_state() == vlc.State.Ended:
            self.play_next()
        elif self.is_playing:
            # Continue checking every second if video is still playing
            self.root.after(1000, self.check_end)
    
    def toggle_play(self):
        # Toggle between play and pause
        if self.player.is_playing():
            self.player.pause()
            self.play_button.config(text="Play")
            self.is_playing = False
        else:
            self.player.play()
            self.play_button.config(text="Pause")
            self.is_playing = True
            # Check video end when playback resumes
            self.update_duration_slider() 
    
    def play_previous(self):
        # Play the previous video in the playlist or a random one if shuffle is enabled
        if self.playlist:
            if self.is_shuffle:
                self.current_index = random.randint(0, len(self.playlist) - 1)
            else:
                self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_current()
    
    def play_selected(self, event=None):
        # Play the video selected in the playlist listbox
        selection = self.playlist_box.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_current()
    
    def set_volume(self, value):
        # Set the volume of the media player
        self.player.audio_set_volume(self.volume_var.get())
    
    def toggle_shuffle(self):
        # Toggle shuffle mode on or off
        self.is_shuffle = not self.is_shuffle
        self.shuffle_button.config(text="Shuffle Off" if self.is_shuffle else "Shuffle On")
    
    def on_closing(self):
        # Stop playback and close the application
        self.player.stop()
        self.root.destroy()
    

    def play_next(self):
        """Plays the next unwatched video, or stops if all are watched."""
        if self.playlist:
            # Loop until we find an unwatched video or have cycled through all
            original_index = self.current_index
            while True:
                # Determine the next index based on shuffle or sequential order
                if self.is_shuffle:
                    self.current_index = random.randint(0, len(self.playlist) - 1)
                else:
                    self.current_index = (self.current_index + 1) % len(self.playlist)
                
                # Check if the video is unwatched or we are back to the start
                if self.current_index not in self.watched_videos or self.current_index == original_index:
                    break
            
            # Play if we found an unwatched video; otherwise, stop playback
            if self.current_index not in self.watched_videos:
                self.play_current()
            
    
    def reset_watched_videos(self):
        """Clears the watched video set, allowing all videos to be played again."""
        self.watched_videos.clear()
    
    def on_duration_change(self, value):
        # Seek to position when slider is moved
        if self.is_playing:
            try:
                position = int(float(value)) * 1000  # Convert to milliseconds
                self.player.set_time(position)
            except Exception as e:
                print(f"Error seeking: {e}")
                
    def update_duration_slider(self):
        if self.is_playing:
            try:
                length = self.player.get_length() // 1000  # Video length in seconds
                position = self.player.get_time() // 1000  # Current position in seconds
                
                if length > 0:
                    # Update slider
                    self.duration_slider.config(to=length)
                    self.duration_var.set(position)
                    
                    # Update timer label
                    self.update_timer_label(position, length)
                
                if self.player.get_state() == vlc.State.Ended:
                    self.play_next()
                else:
                    # Continue updating
                    self.root.after(1000, self.update_duration_slider)
            except Exception as e:
                print(f"Error updating duration: {e}")
                self.root.after(1000, self.update_duration_slider)
    
    
    def update_timer_label(self, position, length):
        # Convert seconds to minutes and seconds
        pos_min, pos_sec = divmod(position, 60)
        len_min, len_sec = divmod(length, 60)
        
        # Update the timer label
        self.timer_label.config(
            text=f"{int(pos_min):02d}:{int(pos_sec):02d} / {int(len_min):02d}:{int(len_sec):02d}"
        )
    
    # Change the Screen Size
    def on_frame_resize(self, event):
        """Handle resizing of the video frame."""
        # you can adjust video playback size here.
        # For example, maintaining an aspect ratio:
        width = event.width
        height = int(width * 9 / 16)  # Example aspect ratio (16:9)
    
        self.video_frame.config(width=width, height=height)
    
    def bind_keys(self):
        """Bind keyboard shortcuts to functions."""
        self.root.bind("<Right>", lambda event: self.skip_forward())  # Right arrow key for forward
        self.root.bind("<Left>", lambda event: self.skip_back()) # Left arrow key for back
        self.root.bind("<Up>", lambda event: self.accélération_lecture())
        self.root.bind("<Down>", lambda event: self.décélération_lecture())

    def skip_forward(self, event=None):
        """Skip forward by 15 seconds."""
        if self.player.is_playing():
            current_time = self.player.get_time()  # Get current playback time in milliseconds
            self.player.set_time(min(current_time + 15000, self.player.get_length()))  # Skip forward 15 seconds

    # As the func_name imply
    def skip_back(self, event=None):
        """Skip backward by 15 seconds."""
        if self.player.is_playing():
            current_time = self.player.get_time()  # Get current playback time in milliseconds
            self.player.set_time(max(current_time - 15000, 0))  # Skip backward 15 seconds

    # As the func_name imply
    def set_speed(self, value):
        """Set the playback speed of the media player."""
        speed = self.speed_var.get()
        self.player.set_rate(speed)
        self.speed_label.config(text=f"Speed: {speed:.1f}x")  # Update speed label
    
    # Acceleration video    
    def décélération_lecture(self, event=None):
        if self.player.is_playing() and self.playback_speed > 0.5:
            self.playback_speed -= 0.1  # décélère
            self.player.set_rate(self.playback_speed)
            self.speed_var.set(self.playback_speed)  # Update slider
            self.speed_label.config(text=f"Speed: {self.playback_speed:.1f}x")
        
    # Deceleration video
    def accélération_lecture(self, event=None):
        if self.player.is_playing() and self.playback_speed < 5:
            self.playback_speed += 0.1 # Accélère
            self.player.set_rate(self.playback_speed)
            self.speed_var.set(self.playback_speed)  # Update slider
            self.speed_label.config(text=f"Speed: {self.playback_speed:.1f}x")
            
        
            
# Initialize and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()
