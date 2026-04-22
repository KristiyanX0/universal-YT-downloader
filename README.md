# Universal YouTube Downloader

A command-line YouTube video and playlist downloader built with Python, `yt-dlp`, and `rich`. My girlfriend asked me to download a huge playlist in a specific folder for something so I just Vibe coded this in two hours.

## Prerequisites

1. **Python 3.8+** installed on your system.
2. **FFmpeg**: You must download the Windows build of `ffmpeg.exe` (from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)) and place it in the root folder of this project before building.

## How to Set Up & Build

I have included batch scripts to completely automate the setup and build process for Windows users.

### Step 1: Install Dependencies

Double-click `setup.bat` (or run it in your terminal).
This will automatically:

- Create a localized Python Virtual Environment (`env/`).
- Install all required packages (`yt-dlp`, `rich`, `pyinstaller`).

### Step 2: Build the Executable

Ensure `ffmpeg.exe` is placed in the same folder as `universal_downloader.py`.
Double-click `build.bat`.
This will:

- Verify FFmpeg is present.
- Use PyInstaller to compile the script and embed `ffmpeg.exe` inside it.
- Output your final, standalone app to `dist\universal_downloader.exe`.

### Step 3: Clean Up (Optional)

If you want to rebuild you should firstly use `clean.bat`.

## Usage

Once built, you can move `universal_downloader.exe` anywhere on your computer.
On its first run, it will automatically generate a `config.json` file where you can customize:

- Download location
- Audio-only extraction mode
- Default video quality formats
