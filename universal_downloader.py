import yt_dlp
import os
import sys
import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn
)

# Initialize the Rich console
console = Console()

# ==========================================
# --- CONFIGURATION MANAGER ---
# ==========================================
CONFIG_FILE = 'config.json'

# Removed the cookie settings from the default config entirely
DEFAULT_CONFIG = {
    "download_folder": "./Downloaded Content",
    "default_format": "best",
    "extract_audio_only": False
}

def load_config():
    """Loads the config file. If it doesn't exist, creates it automatically."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except Exception:
        console.print("[bold red]⚠️ Config file is corrupted! Using defaults.[/bold red]")
        return DEFAULT_CONFIG

config = load_config()

# ==========================================
# --- CORE APP ---
# ==========================================
def get_ffmpeg_path():
    """Finds the bundled ffmpeg when running as an .exe"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return '.'

class RichLogger:
    def debug(self, msg): 
        pass
    def warning(self, msg): 
        if "JavaScript runtime" in msg:
            return
        console.print(f"[bold yellow]⚠️ WARNING:[/bold yellow] {msg}")
    def error(self, msg): 
        console.print(f"[bold red]❌ ERROR:[/bold red] {msg}")

def download_youtube_content(url):
    output_folder = config.get('download_folder', './Downloaded Content')
    os.makedirs(output_folder, exist_ok=True)

    is_playlist = 'list=' in url

    if is_playlist:
        console.print("\n[bold cyan]📁 Playlist link detected![/bold cyan]")
        output_template = os.path.join(output_folder, '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s')
        prevent_playlist = False
    else:
        console.print("\n[bold magenta]🎬 Single video link detected![/bold magenta]")
        output_template = os.path.join(output_folder, '%(title)s.%(ext)s')
        prevent_playlist = True

    # --- SETUP THE RICH PROGRESS BAR ---
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        expand=True
    )
    
    # 🧠 Dictionary to keep track of multiple progress lines!
    current_tasks = {}

    def progress_hook(d):
        # We use the raw filename as the unique ID for the dictionary
        filename_raw = d.get('filename', 'video')
        
        # We make a clean, short version for the terminal display
        display_name = os.path.basename(filename_raw)
        if len(display_name) > 35:
            display_name = display_name[:32] + "..."

        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            
            # If we haven't seen this file yet, create a BRAND NEW progress line for it
            if filename_raw not in current_tasks:
                task_id = progress.add_task(f"[cyan]Downloading:[/cyan] {display_name}", total=total or 100)
                current_tasks[filename_raw] = task_id
                
            task_id = current_tasks[filename_raw]
            
            if total:
                progress.update(task_id, completed=downloaded, total=total)
            else:
                progress.update(task_id, completed=downloaded)
                
        elif d['status'] == 'finished':
            if filename_raw in current_tasks:
                task_id = current_tasks[filename_raw]
                # Lock it at 100% and turn it green permanently
                progress.update(task_id, completed=d.get('total_bytes') or d.get('downloaded_bytes', 100), description=f"[bold green]✅ Downloaded:[/bold green] {display_name}")

    # --- DYNAMIC YT-DLP OPTIONS ---
    ydl_opts = {
        'outtmpl': output_template,
        'ignoreerrors': True,
        'noplaylist': prevent_playlist,
        'ffmpeg_location': get_ffmpeg_path(), 
        'logger': RichLogger(),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'noprogress': True
    }

    # Apply Audio vs Video config
    if config.get('extract_audio_only', False):
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        console.print("[dim]🎵 Audio Only Mode Enabled[/dim]")
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts['merge_output_format'] = 'mp4'

    console.print("\n[dim]Fetching video metadata and starting engine...[/dim]\n")
    
    try:
        with progress:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
        console.print("\n[bold green]✅ Operation completed successfully![/bold green]\n")
    except Exception as e:
        console.print(f"\n[bold red]❌ A critical error occurred:[/bold red] {e}\n")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    welcome_panel = Panel(
        "[bold white]Universal YouTube Downloader[/bold white]\n[dim]Powered by yt-dlp & FFmpeg[/dim]",
        style="blue",
        expand=False,
        border_style="cyan"
    )
    console.print(welcome_panel)
    
    user_url = Prompt.ask("\n[bold yellow]Enter a YouTube link (Single Video OR Playlist)[/bold yellow]").strip()
    
    if user_url:
        download_youtube_content(user_url)
    else:
        console.print("[dim]No URL provided. Exiting.[/dim]")
        
    Prompt.ask("\n[dim]Press Enter to close...[/dim]")