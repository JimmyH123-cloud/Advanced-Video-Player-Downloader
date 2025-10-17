import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import vlc
import random
import traceback
from pathlib import Path
import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFont
from functools import lru_cache
import ast
import time

import platform
import ctypes

class VideoPlayer:
     
    PREVIEW_WIDTH = 200 # Preview video Width
    PREVIEW_HEIGHT = 120 # Preview video Height
    SKIP_TIME = 15000 # Set the skip time to 15s
    MAX_PLAYBACK_SPEED = 4.0
    
    def __init__(self, root):
        
        # Initialize the main window
        self.root = root
        self.root.title("Video Playlist Player")

        screen_width = root.winfo_screenwidth()
        # screen_height = root.winfo_screenheight()

        # Set consistent window sizing for Linux and macOS
        self.window_width = max(1200, min(1400, int(screen_width * 0.5)))
        self.window_height = max(700, int(self.window_width / (16/9)))

        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.minsize(900, 550)
       
        
        system = platform.system()
        print(f"Detected OS: {system}")

        vlc_args = [
            '--quiet',
            '--no-video-title-show',
            '--no-disable-screensaver',
        ]

        if system == "Linux":
            vlc_args += ['--aout=pulse']
        elif system == "Darwin":  # macOS
            vlc_args += ['--aout=auhal']
        
        # Initialize VLC instance and media player
        self.instance = vlc.Instance(vlc_args)
        self.player = self.instance.media_player_new()
        
        # Initialize playlist attributes
        self.playlist = []
        self.is_playing = False # For toggle play/pause logic
        self.is_shuffle = True # For toggle random/stactic next video logic
        self.playback_speed = 1.0
        self.previous_index = 0
        self.watched_videos = set()
        
        self.last_hover_time = 0
        self.hover_cooldown = 0.1 # 10ms cooldown between hover events to reduce `computationnal comsuption`.
        
        # Load platform-appropriate font
        self._load_font()
        
        # Setup the user interface
        self._vlc_bound = False
        self.setup_ui()
        self.bind_keys()
        
        # Bind close window event to stop playback
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def _load_font(self):
        """Load platform-appropriate font"""
        try:
            system = platform.system()
            if system == "Linux":
                self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
            elif system == "Darwin":
                self.font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 16)
            else:
                self.font = ImageFont.load_default()
        except Exception:
            self.font = ImageFont.load_default()
        
    def setup_ui(self):
        
        # Create main container frame
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=7, pady=4)
        
        # Create Preview image
        self.preview_image_label = ttk.Label(self.root)
        self.preview_image_label.place_forget()
        
        # Create video display frame
        self.video_frame = ttk.Frame(self.main_container, borderwidth=2, relief='solid')
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Set the desired aspect ratio for the video
        self.video_frame.pack_propagate(False)
        self.video_frame.config(width=int(self.window_width), height=int(self.window_height * 0.6))
               
        # Create a container for preview and slider
        preview_container = ttk.Frame(self.main_container)
        preview_container.pack(fill=tk.X, padx=5, pady=5)

        # Duration slider
        self.duration_var = tk.DoubleVar()
        self.duration_slider = ttk.Scale(
            preview_container, from_=0, to=100, orient=tk.HORIZONTAL,
            variable=self.duration_var, command=self.on_duration_change
        )
        self.duration_slider.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Bind slider events for preview
        self.duration_slider.bind('<Motion>', self.show_preview)
        self.duration_slider.bind('<Leave>', self.hide_preview)

        # Timer label
        self.timer_label = ttk.Label(self.main_container, text="00:00 / 00:00")
        self.timer_label.pack(pady=5)

        # Control buttons
        controls = ttk.Frame(self.main_container)
        controls.pack(fill=tk.X, pady=4)

        ttk.Button(controls, text="Select Folder", command=self.load_folder).pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Previous", command=self.play_previous, width=7.5).pack(side=tk.LEFT, padx=2, pady=2)
        self.play_button = ttk.Button(controls, text="Play", command=self.toggle_play, width=5)
        self.play_button.pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(controls, text="Next", command=self.play_next, width=5).pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Button(controls, text=f"<-- {self.SKIP_TIME * 0.001:.0f}s", command=self.skip_back, width=8).pack(side=tk.LEFT)
        ttk.Button(controls, text=f"--> {self.SKIP_TIME * 0.001:.0f}s", command=self.skip_forward, width=8).pack(side=tk.LEFT)

        ttk.Button(controls, text="RTWV", command=self.reset_watched_videos, width=6.5).pack(side=tk.LEFT, padx=2, pady=2)

        self.shuffle_button = ttk.Button(controls, text="Shuffle Off" if self.is_shuffle else "Shuffle On", command=self.toggle_shuffle)
        self.shuffle_button.pack(side=tk.LEFT, padx=4)

        self.volume_var = tk.IntVar(value=50)
        volume_slider = ttk.Scale(controls, from_=0, to=100, orient=tk.HORIZONTAL,
                                  variable=self.volume_var, command=self.set_volume)
        volume_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Playlist display frame
        playlist_frame = ttk.Frame(self.main_container)
        playlist_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.playlist_box = tk.Listbox(playlist_frame, selectmode=tk.SINGLE)
        self.playlist_box.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=self.playlist_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist_box.config(yscrollcommand=scrollbar.set)

        self.speed_var = tk.DoubleVar(value=1.0)
        speed_slider = ttk.Scale(controls, from_=0.5, to=2.0, orient=tk.HORIZONTAL,
                        variable=self.speed_var, command=self.set_speed)
        speed_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.speed_label = ttk.Label(controls, text="Speed: 1.0x")
        self.speed_label.pack(side=tk.LEFT)

        self.playlist_box.bind('<Double-Button-1>', self.play_selected)
        self.duration_slider.bind("<Button-1>", self.duration_bar_click)
        
        # Menu bar
        menubar = tk.Menu(self.root) 
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load Watched Videos", command=self.load_previous_tracked)
        filemenu.add_command(label="Save Watched Videos", command=self.save_watched_videos)
        menubar.add_cascade(label="File", menu=filemenu)
        
        subtitlemenu = tk.Menu(menubar, tearoff=0)
        subtitlemenu.add_command(label="Enable Subtitles", command=self.enable_subtitles)
        subtitlemenu.add_command(label="Disable Subtitles", command=self.disable_subtitles)
        subtitlemenu.add_command(label="Select Subtitle Track", command=self.select_subtitle_track)
        menubar.add_cascade(label="Subtitles", menu=subtitlemenu)
        self.root.config(menu=menubar) 

    def bind_vlc_window(self):
        """Bind the VLC player window to the Tk widget"""
        if self._vlc_bound:
            return

        wid = self.video_frame.winfo_id()
        system = platform.system()
        
        try:
            if system == "Linux":
                self.player.set_xwindow(wid)
            elif system == "Darwin":
                # macOS requires the pointer to be wrapped
                self.player.set_nsobject(ctypes.c_void_p(wid))
            self._vlc_bound = True
            print(f"VLC window bound successfully on {system}")
        except Exception as e:
            print(f"Failed to bind VLC window: {e}")
            traceback.print_exc()

    def load_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.bind_vlc_window()
            
            self.playlist.clear()
            self.playlist_box.delete(0, tk.END)
            
            for file in sorted(Path(folder).glob("*.mp4")):
                self.playlist.append(str(file))
                self.playlist_box.insert(tk.END, file.name)
            
            if self.playlist:
                self.player.audio_set_volume(self.volume_var.get())
                self.current_index = 0
                self.watched_videos.clear()
                self.play_current()

    def play_current(self):
        if not (0 <= self.current_index < len(self.playlist)):
            return
        
        self.media = self.instance.media_new(self.playlist[self.current_index])
        self.media.parse_with_options(vlc.MediaParseFlag.local, -1)
        self.player.set_media(self.media)
        
        self.player.play()
        self.is_playing = True
        self.play_button.config(text="Pause")
        
        # Schedule subtitle parsing
        self.root.after(500, lambda: self._update_subtitle_tracks())
    
        # Update the playlist UI
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(self.current_index)
        self.playlist_box.see(self.current_index)
        
        # Mark the video as watched
        self.watched_videos.add(self.current_index)
        
        # Update the duration slider
        self.update_duration_slider()
        
        # Disable previous video subtitle by default
        self.disable_subtitles()
        
        print(f"""
        {"=" * 55}
        || {'Current Video Watching:':^49} ||
        || {os.path.basename(self.playlist[self.current_index]):^49} ||
        {"=" * 55}
        """)
    
    def _update_subtitle_tracks(self):
        """Update subtitle tracks list"""
        self.subtitle_tracks = self.get_subtitle_tracks()
    
    def toggle_play(self, event=None):
        if self.player.is_playing():
            self.player.pause()
            self.play_button.config(text="Play")
            print(f"""\nset of self.watched_video:|-> {self.watched_videos} <-| \nand title watched:  {[os.path.basename(self.playlist[i]) for i in self.watched_videos]}""")   
        else:
            self.player.play()
            self.play_button.config(text="Pause")
            self.is_playing = self.player.is_playing()
            self.update_duration_slider()

    def play_previous(self):
        if self.playlist and self.previous_index != self.current_index:
            self.watched_videos.discard(self.current_index)
            self.current_index = self.previous_index
            self.play_current()

    def play_selected(self, event=None):
        selection = self.playlist_box.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_current()
    
    def duration_bar_click(self, event):
        """Handle clicks on the duration bar"""
        if self.player.get_length() > 0:
            slider_width = self.duration_slider.winfo_width()
            if slider_width > 0:
                total_duration = self.player.get_length() / 1000
                mouse_relative_pos = event.x / slider_width
                click_time = int(mouse_relative_pos * total_duration)
                self.player.set_time(click_time * 1000) 
                self.update_duration_slider() 
            
    def set_volume(self, value):
        self.player.audio_set_volume(self.volume_var.get())

    def toggle_shuffle(self):
        self.is_shuffle = not self.is_shuffle # apply "not" and change the boolean value
        self.shuffle_button.config(text="Shuffle Off" if self.is_shuffle else "Shuffle On")

    def on_closing(self):
        if hasattr(self, 'media'):
            self.media.release() 
            del self.media 
        self.player.stop()
        self.player.release()
        del self.player
        self.root.destroy()

    def play_next(self):
        if not self.playlist:
            return
        
        original_index = self.current_index
        self.previous_index = self.current_index
        
        while True:
            if self.is_shuffle:
                while True:
                    self.current_index = random.randint(0, len(self.playlist) - 1)
                    if self.current_index not in self.watched_videos or len(self.watched_videos) == len(self.playlist):
                        break
            else:
                self.current_index = (self.current_index + 1) % len(self.playlist)
            
            if self.current_index not in self.watched_videos or original_index == self.current_index or len(self.watched_videos) == len(self.playlist):
                print("Please press the 'RTWV' as there are no unwatched video currently")
                break
        
        if self.current_index not in self.watched_videos:
            self.play_current()

    def reset_watched_videos(self):
        self.watched_videos.clear()
        print(f"{'The Watched Videos Tracker has been reset!'.upper()} \n{'you can proceed.'.upper()}")
    
    def on_duration_change(self, value):
        if self.is_playing and self.player.get_length() > 0:
            try:
                position = int(float(value)) * 1000
                self.player.set_time(position)
            except Exception as e:
                print(f"Error seeking: {e}")

    def update_duration_slider(self):
        if not self.is_playing:
            return
    
        try:
            length = self.player.get_length() // 1000
            position = self.player.get_time() // 1000
        
            if length > 0:
                self.duration_slider.config(to=length)
                self.duration_var.set(position)
                self.update_timer_label(position, length)
            
            if self.player.get_state() == vlc.State.Ended:
                self.play_next()
            else:
                # Check for significant time jumps (more than 1 second)
                if abs(self.duration_var.get() - position) > 1:
                    self.duration_var.set(position) # Correct the slider if there is a jump
                    self.update_timer_label(position, length)
                self.root.after(250, self.update_duration_slider)
        except (vlc.VlcError, AttributeError, ZeroDivisionError) as e:
            print(f"Error updating duration: {e}")
            self.root.after(1000, self.update_duration_slider)
    
    def update_timer_label(self, position, length):
        pos_min, pos_sec = divmod(position, 60)
        len_min, len_sec = divmod(length, 60)
        
        self.timer_label.config(
            text=f"{int(pos_min):02d}:{int(pos_sec):02d} / {int(len_min):02d}:{int(len_sec):02d}"
        )
    
    def show_preview(self, event):
        """Show the preview video on hover"""
        current_time = time.time()
        if current_time - self.last_hover_time < self.hover_cooldown:
            return # Skip if still in cooldown
        
        try:
            if self.playlist and self.player.get_length() > 0: # Check if video loaded
                current_media = self.playlist[self.current_index]
                total_duration = self.player.get_length() / 1000
                slider_width = self.duration_slider.winfo_width()
                mouse_relative_pos = event.x / slider_width
                preview_time = int(mouse_relative_pos * total_duration)

                preview_image = self.generate_video_preview(current_media, preview_time)

                if preview_image is not None:
                    minutes, seconds = divmod(preview_time, 60)
                    preview_text = f"{minutes:02d}:{seconds:02d}"
                    preview_with_time = self.create_preview_composite(preview_image, preview_text)
                    photo = ImageTk.PhotoImage(preview_with_time)

                    self.preview_image_label.config(image=photo)
                    self.preview_image_label.image = photo

                    mouse_x = self.root.winfo_pointerx()
                    relative_mouse_x = mouse_x - self.root.winfo_rootx()

                    preview_x = relative_mouse_x - (self.PREVIEW_WIDTH // 2)
                    slider_y_relative_to_root = self.duration_slider.winfo_rooty() - self.root.winfo_rooty()
                    preview_y = slider_y_relative_to_root - self.PREVIEW_HEIGHT - 10
                    
                    preview_x = max(0, min(preview_x, self.root.winfo_width() - self.PREVIEW_WIDTH))
                    preview_y = max(0, preview_y)

                    self.preview_image_label.place(x=preview_x, y=preview_y, width=self.PREVIEW_WIDTH, height=self.PREVIEW_HEIGHT)
                    self.preview_image_label.lift()
        except Exception as e:
            print(f"Preview error: {e}")
            
        self.last_hover_time = current_time
    
    @lru_cache(maxsize=32) # Cache up to 32 recent previews
    def generate_video_preview(self, video_path, timestamp):
        """Generate a preview frame from the video at the specified timestamp"""
        cap = None
        try:
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            
            for _ in range(5): # Skip a few frames to stabilize the decode
                cap.grab()
            
            ret, frame = cap.read()
            if ret:
                frame_resized = cv2.resize(frame, (200, 120), interpolation=cv2.INTER_AREA)
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                preview_image = Image.fromarray(frame_rgb)
                return preview_image
            return None # Return None if there is no frame to avoid further error
        except Exception as e:
            print(f"Error generating preview: {e}")
            return None
        finally:
            if cap is not None:
                cap.release()
    
    def create_preview_composite(self, preview_image, timestamp_text):
        """Create a composite image with preview and timestamp"""
        # Create a new image with a dark background
        composite = Image.new('RGB', (200, 120), color=(0, 0, 0))
        
        # Paste the preview image
        composite.paste(preview_image, (0, 0))
        
        # Add timestamp text
        draw = ImageDraw.Draw(composite)
        
        # Draw text with a semi-transparent background
        text_bbox = draw.textbbox((0, 0), timestamp_text, font=self.font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Draw semi-transparent background for text
        draw.rectangle([0, 0, text_width + 10, text_height + 10], 
                       fill=(0, 0, 0, 128))
        
        # Draw text
        draw.text((5, 5), timestamp_text, font=self.font, fill=(255, 255, 255))
        
        return composite

    def hide_preview(self, event):
        """Hide the preview image"""
        self.preview_image_label.place_forget()

        
    def bind_keys(self):
        self.root.bind("<Right>", lambda event: self.skip_forward())
        self.root.bind("<Left>", self.skip_back)
        self.root.bind("<Up>", self.speed_up)
        self.root.bind("<Down>", self.speed_down)
        self.root.bind("<p>", self.previous_tracked)

    def skip_forward(self, event=None):
        if self.player.is_playing():
            current_time = self.player.get_time()
            self.player.set_time(min(current_time + self.SKIP_TIME, self.player.get_length()))

    def skip_back(self, event=None):
        if self.player.is_playing():
            current_time = self.player.get_time()
            self.player.set_time(max(current_time - self.SKIP_TIME, 0))

    def set_speed(self, value):
        speed = min(self.speed_var.get(), self.MAX_PLAYBACK_SPEED)
        self.speed_var.set(speed)
        self.player.set_rate(speed)
        self.speed_label.config(text=f"Speed: {speed:.1f}x")

    def speed_up(self, event=None):
        if self.player.is_playing() and self.playback_speed < self.MAX_PLAYBACK_SPEED:
            self.playback_speed = min(self.playback_speed + 0.1, self.MAX_PLAYBACK_SPEED)
            self.player.set_rate(self.playback_speed)
            self.speed_var.set(self.playback_speed)
            self.speed_label.config(text=f"Speed: {self.playback_speed:.1f}x")
        
    def speed_down(self, event=None):
        if self.player.is_playing() and self.playback_speed > 0.5:
            self.playback_speed -= 0.1
            self.player.set_rate(self.playback_speed)
            self.speed_var.set(self.playback_speed)
            self.speed_label.config(text=f"Speed: {self.playback_speed:.1f}x")
    
    def get_subtitle_tracks(self):
        """Get a list of available subtitle tracks"""
        tracks = []
        try:
            spu_count = self.player.video_get_spu_count()
            print(f"Total subtitle tracks: {spu_count}")
            
            # Get the list of subtitle track descriptions
            descriptions = self.player.video_get_spu_description()
            
            for i in range(spu_count):
                if i < len(descriptions):
                    track_id, track_name = descriptions[i]
                    track_name = track_name.decode('utf-8') if isinstance(track_name, bytes) else track_name
                    tracks.append((track_id, track_name)) # (track_id, track_name)
        except Exception as e:
            print(f"Error getting subtitle tracks: {e}")
        
        return tracks
    
    def enable_subtitles(self):
        """Enable the first available subtitle track"""
        if self.subtitle_tracks:
            self.player.video_set_spu(self.subtitle_tracks[0][0]) # Enable the first track
            print(f"Subtitles enabled: {self.subtitle_tracks[0][1]}")
        else:
            print("No subtitles available.")

    def disable_subtitles(self):
        """Disable subtitles"""
        try:
            self.player.video_set_spu(-1) # Disable subtitles
            print("Subtitles disabled.")
        except Exception as e:
            print(f"Error disabling subtitles: {e}")
    
    def select_subtitle_track(self):
        """Open a dialog to select a subtitle track"""
        if not self.subtitle_tracks:
            messagebox.showinfo("No Subtitles", "No subtitle tracks available.")
            return

        # Create a dialog to select a subtitle track
        track_dialog = tk.Toplevel(self.root)
        track_dialog.title("Select Subtitle Track")
        track_dialog.geometry("300x200")

        tk.Label(track_dialog, text="Choose a subtitle track:").pack(pady=10)

        track_names = [track[1] for track in self.subtitle_tracks] # Extract track names for the dropdown menu

        # Dropdown menu for subtitle tracks
        selected_track = tk.StringVar(track_dialog)
        selected_track.set(track_names[0]) # Default to the first track
        track_menu = tk.OptionMenu(track_dialog, selected_track, *track_names)
        track_menu.pack(pady=10)

        # Button to confirm selection
        def on_select():
            track_name = selected_track.get() # This is a string
            try:
                # Find the track ID for the selected track name
                track_id = next(track[0] for track in self.subtitle_tracks if track[1] == track_name)
                self.player.video_set_spu(track_id)
                print(f"Selected subtitle track: {track_name}")
            except StopIteration:
                print(f"Subtitle track '{track_name}' not found.")
            track_dialog.destroy()

        tk.Button(track_dialog, text="Select", command=on_select).pack(pady=10)
    
    def load_previous_tracked(self): # Separate function for loading logic
        """Load watched videos from file"""
        if not self.playlist:
            return

        playlist_length = len(self.playlist)
        valid_indices = set(range(playlist_length))
        filepath = Path("watched_videos.txt")

        if not filepath.exists():
            try:
                with open(filepath, "w") as f:
                    f.write(str(set()))
            except Exception as e:
                messagebox.showerror("Error", f"Error creating watched videos file: {e}")
                return

        try:
            with open(filepath, "r") as f:
                try:
                    loaded_tracked = ast.literal_eval(f.read())
                    if isinstance(loaded_tracked, set):
                        invalid_indices = loaded_tracked - valid_indices # Find invalid indices
                        if invalid_indices:
                            message = f"Some tracked videos are not in the current playlist: {invalid_indices}. They will be ignored."
                            messagebox.showwarning("Warning", message)
                            loaded_tracked &= valid_indices # Keep only valid indices equivalent to intersection = set1 & set2
                            self.watched_videos.update(loaded_tracked)
                        elif loaded_tracked.issubset(valid_indices):
                            self.watched_videos.update(loaded_tracked)
                            messagebox.showinfo("Success", "Tracked videos successfully loaded.")
                        return
                    else:
                        messagebox.showerror("Error", "Invalid data in tracked videos file. Resetting watched list.")
                        self.watched_videos = set()
                        with open(filepath, "w") as f:
                            f.write(str(set()))
                except (SyntaxError, ValueError):
                    messagebox.showerror("Error", "Invalid format in tracked videos file. Resetting watched list.")
                    self.watched_videos = set()
                    with open(filepath, "w") as f:
                        f.write(str(set()))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading tracked videos: {e}")
    
    def save_watched_videos(self):
        """Save watched videos to file"""
        filepath = Path("watched_videos.txt")
        try:
            with open(filepath, "w") as f:
                f.write(str(self.watched_videos))
            messagebox.showinfo("Success", f"Watched videos saved to: {filepath.absolute()}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving watched videos: {e}")
    
    # Keep tracked of your last session.
    def previous_tracked(self, event=None):
        if not self.playlist:
            return

        playlist_length = len(self.playlist)
        valid_indices = set(range(playlist_length))
        filepath = Path("watched_videos.txt")
        save_response = messagebox.askyesno("Save Current Session?", "Do you want to SAVE tracked videos from Current session?")

        if event and event.keysym.lower() == "p" and save_response:
            print("parsing...")
            try:
                with open(filepath, "w") as f:
                    f.write(str(self.watched_videos))
                messagebox.showinfo("Success", "Watched videos saved.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving watched videos: {e}")
            return

        # Check if file exists. Create it with an empty set if it doesn't.
        if not filepath.exists():
            try:
                with open(filepath, "w") as f:
                    f.write(str(set()))  # Initialize with an empty set
            except Exception as e:
                messagebox.showerror("Error", f"Error creating watched videos file: {e}")
                return # Exit if file creation fails

        load_response = messagebox.askyesno("Load Previous Session?", "Do you want to LOAD tracked videos from a previous session?")

        if load_response:
            try:
                with open(filepath, "r") as f:
                    try:
                        loaded_tracked = ast.literal_eval(f.read())
                        if isinstance(loaded_tracked, set) and loaded_tracked.issubset(valid_indices):
                            self.watched_videos.update(loaded_tracked)
                            messagebox.showinfo("Success", "Tracked videos successfully loaded.")
                            return
                        else:
                            messagebox.showerror("Error", "Invalid data in tracked videos file. Reseting watched list.")
                            self.watched_videos = set() # reset the watched list
                            with open(filepath, "w") as f: # write the empty set to the file
                                f.write(str(set()))
                    except (SyntaxError, ValueError):
                        messagebox.showerror("Error", "Invalid format in tracked videos file. Reseting watched list.")
                        self.watched_videos = set() # reset the watched list
                        with open(filepath, "w") as f: # write the empty set to the file
                                f.write(str(set()))
            except Exception as e:
                messagebox.showerror("Error", f"Error loading tracked videos: {e}")

        print("Program resume.")

        
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()
