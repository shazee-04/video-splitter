import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import ttkbootstrap as tb  # Import the ttkbootstrap package
import os
from moviepy.editor import VideoFileClip
import threading
from PIL import Image, ImageTk  # Import Pillow

# Custom MessageBox class
class CustomMessageBox(tk.Toplevel):
    def __init__(self, title, message, icon=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        if icon:
            self.iconphoto(False, icon)
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set()

        # Create widgets
        msg_label = ttk.Label(self, text=message, wraplength=250)
        ok_button = ttk.Button(self, text="OK", command=self.destroy)

        # Layout
        msg_label.pack(pady=20)
        ok_button.pack(pady=10)

        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) // 2
        self.geometry(f"+{x}+{y}")

def show_custom_info(title, message):
    CustomMessageBox(title, message, icon)

def show_custom_error(title, message):
    CustomMessageBox(title, message, icon)

def browse_video():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if selected_file_path:
        video_label.config(text=f"Selected Video: {selected_file_path}")

def split_video():
    if not selected_file_path:
        show_custom_error("Error", "No video file selected!")
        return

    try:
        minutes = int(minutes_entry.get())
        seconds = int(seconds_entry.get())
        part_length = minutes * 60 + seconds
    except ValueError:
        show_custom_error("Error", "Invalid time input!")
        return

    # Disable UI elements
    set_ui_state("disabled")
    
    threading.Thread(target=process_video, args=(part_length,)).start()

def process_video(part_length):
    try:
        video = VideoFileClip(selected_file_path)
        duration = video.duration
        start_times = list(range(0, int(duration), int(part_length)))
        
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        video_name = os.path.splitext(os.path.basename(selected_file_path))[0]
        video_output_dir = os.path.join(output_dir, video_name)
        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)
        
        progress_bar['maximum'] = len(start_times)
        for idx, start_time in enumerate(start_times):
            end_time = min(start_time + part_length, duration)
            video_part = video.subclip(start_time, end_time)
            if video_part is None:
                raise ValueError(f"Failed to create video part for segment {idx + 1}.")
            output_path = os.path.join(video_output_dir, f"part_{idx+1}.mp4")
            video_part.write_videofile(output_path, codec="libx264")
            progress_bar['value'] = idx + 1
            progress_label.config(text=f"Progress: {idx + 1}/{len(start_times)}")
        
        show_custom_info("Success", "Video split successfully!")
    except Exception as e:
        show_custom_error("Error", f"An error occurred: {str(e)}")
    finally:
        # Re-enable UI elements
        set_ui_state("normal")

def set_ui_state(state):
    browse_button['state'] = state
    minutes_entry['state'] = state
    seconds_entry['state'] = state
    split_button['state'] = state

selected_file_path = None

# Creating the main application window
app = tb.Window(themename="cyborg")  # Replace "cyborg" with an available theme name
app.title("Video Splitter")

# Load the icon once
icon_path = os.path.join(os.path.dirname(__file__), "video1.ico")
if os.path.exists(icon_path):
    icon_image = Image.open(icon_path)
    icon = ImageTk.PhotoImage(icon_image)
else:
    icon = None
    print(f"Icon file not found: {icon_path}")

# Set the icon for the main window
if icon:
    app.iconphoto(False, icon)

# Set window size to 60% of screen width and 50% of screen height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = int(screen_width * 0.5)
window_height = int(screen_height * 0.5)
app.geometry(f"{window_width}x{window_height}")

# Center the content
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Define styles
style = ttk.Style(app)
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 11), padding=10)
style.configure("TEntry", font=("Arial", 12), padding=5)
style.configure("TFrame")

# Create a frame to hold all widgets and apply the frame style
frame = ttk.Frame(app, style="TFrame")
frame.grid(row=0, column=0, sticky="nsew", padx=260, pady=50)
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(4, weight=1)
frame.grid_rowconfigure(5, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Add Browse button to select video file
browse_button = ttk.Button(frame, text="Browse", command=browse_video, style="TButton")
browse_button.grid(row=0, column=0, columnspan=2, pady=10)

# Add label to display selected video file
video_label = ttk.Label(frame, text="No video selected", style="TLabel")
video_label.grid(row=1, column=0, columnspan=2, pady=10)

# Add input fields and labels for part length (minutes and seconds)
minutes_label = ttk.Label(frame, text="Split Length (min):", style="TLabel")
minutes_label.grid(row=2, column=0, sticky='e', pady=10)
minutes_entry = ttk.Entry(frame, style="TEntry")
minutes_entry.grid(row=2, column=1, sticky='w', pady=10)

seconds_label = ttk.Label(frame, text="Split Length (sec):", style="TLabel")
seconds_label.grid(row=3, column=0, sticky='e', pady=10)
seconds_entry = ttk.Entry(frame, style="TEntry")
seconds_entry.grid(row=3, column=1, sticky='w', pady=10)

# Add Split button to start splitting the video
split_button = ttk.Button(frame, text="Split", command=split_video, style="TButton")
split_button.grid(row=4, column=0, columnspan=2, pady=20)

# Add a progress bar
progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate", length=200)
progress_bar.grid(row=5, column=0, columnspan=2, pady=10)

# Add a label to show the progress
progress_label = ttk.Label(frame, text="Progress: 0/0", style="TLabel")
progress_label.grid(row=6, column=0, columnspan=2, pady=0)

# Run the application
app.mainloop()
