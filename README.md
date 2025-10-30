[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)

<div align="center">
	<img src="https://github.com/user-attachments/assets/4d90e082-33c0-470c-b162-34e0b3a55cdc" alt="Video Splitter Preview" width="100%" />
</div>

### Overview

Video Splitter is a lightweight desktop GUI built with Python (Tkinter + ttkbootstrap) that lets you split a video into equal-length parts in just a few clicks. Pick a file, set the desired length in minutes/seconds, and the app exports sequential MP4 parts to an output folder.

##

### Features

- Simple, modern UI using ttkbootstrap themes
- Select a video file and split by fixed duration (minutes + seconds)
- Background processing to keep the UI responsive
- Visual progress bar and progress counter
- Outputs H.264 MP4 files named sequentially (part_1.mp4, part_2.mp4, ...)
- Organizes results per video under output/<video_name>/

##

### Requirements

- Python 3.9 or newer
- OS: Windows, macOS, or Linux
- FFmpeg: moviepy uses imageio-ffmpeg to download a compatible FFmpeg binary automatically if one isn’t found. Installing FFmpeg system-wide can speed up processing and avoid extra downloads.

##

### Installation

Use a virtual environment and install the required Python packages.

#### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

#### macOS/Linux (bash/zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

##

### Usage

#### Start the app

```powershell
python app.py
```

#### Workflow

1. Click Browse and choose a video file (.mp4, .avi)
2. Enter the split length as minutes and seconds
3. Click Split to start processing
4. Monitor progress; when complete, parts are saved to:
	 - output/<video_name>/part_1.mp4, part_2.mp4, ...

#### Notes

- Supported inputs: common formats supported by moviepy/FFmpeg (.mp4, .avi)
- Output is MP4 (H.264 codec)
- Very large files may take time; ensure adequate disk space

#### Troubleshooting

- If FFmpeg isn’t found, moviepy will attempt to download a compatible binary automatically via imageio-ffmpeg.
- If the window icon doesn’t show, ensure favicon.ico exists in the project root.

##

### Technologies

- Python, Tkinter, ttkbootstrap
- moviepy (video reading/writing, splitting)
- Pillow (PIL) for icon handling
- threading (run processing without freezing UI)

##

### Configuration

- Theme: the app uses the ttkbootstrap theme "cyborg" by default. You can change it in app.py: `tb.Window(themename="cyborg")`.
- Output folder: created automatically under output/<video_name>/ relative to the project root.
- Supported input formats are determined by moviepy/FFmpeg; add more filetypes in `filedialog.askopenfilename` if needed.

##

### Repository Structure

```text
video-splitter/
├─ app.py                  # Main GUI application (Tkinter + ttkbootstrap + moviepy)
├─ favicon.ico             # Window icon used by the application and banner image above
├─ README.md               # Project documentation (you are here)
├─ requirements.txt        # Python dependencies for this application
```

#### What each part does

- `app.py`: Implements the GUI, file selection, duration inputs, background splitting, and progress updates.
- `favicon.ico`: Icon for the application window; also displayed at the top of this README.
- `README.md`: Usage, installation, and contributor info.
- `.github/prompts/create-readme.prompt.md`: Meta-prompt describing how this README is generated; not required to run the app.

##

### Contributing

Contributions are welcome. To propose a change:

1. Fork the repository and create a feature branch
2. Make your changes with clear commit messages
3. Test locally on a sample video
4. Open a Pull Request describing the change and rationale

For issues or feature requests, please open a GitHub Issue.

##

### Documentation

- moviepy: https://zulko.github.io/moviepy/
- ttkbootstrap: https://ttkbootstrap.readthedocs.io/
- Pillow: https://pillow.readthedocs.io/

##

### Acknowledgements

- moviepy and imageio-ffmpeg for video processing
- ttkbootstrap for the modern Tkinter theme
- Pillow for image/icon handling