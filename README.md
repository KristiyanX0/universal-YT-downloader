# Universal YouTube Downloader

#### [📥 CLICK HERE TO DOWNLOAD THE .EXE](https://github.com/KristiyanX0/universal-YT-downloader/releases/latest)

_(No installation or coding required! Just download the `.exe` and run it.)_

---

A powerful, command-line YouTube video and playlist downloader built with Python, `yt-dlp`, and `rich`. It features a modern terminal UI, auto-generated configuration files, and seamless audio extraction.

## Prerequisites (For Developers Building from Source)

1. **Python 3.8+** installed on your system.
2. **FFmpeg**: You must download the Windows build of `ffmpeg.exe` (from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)) and place it in the root folder of this project before building.

## How to Set Up & Build

We have included batch scripts to completely automate the setup and build process for Windows users.

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

If you want to build again firstly use `clean.bat`.

## Usage

Once built or downloaded, you can move `universal_downloader.exe` anywhere on your computer.
On its first run, it will automatically generate a `config.json` file where you can customize:

- Download location
- Audio-only extraction mode
- Default video quality formats
