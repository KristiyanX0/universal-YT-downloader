@echo off
echo Building universal_downloader...

if not exist ffmpeg.exe (
    echo ERROR: ffmpeg.exe not found in current directory.
    exit /b 1
)

pyinstaller --onefile --add-binary "ffmpeg.exe;." universal_downloader.py

if %errorlevel% equ 0 (
    echo.
    echo Build successful! Executable is in dist\universal_downloader.exe
) else (
    echo.
    echo Build failed.
    exit /b %errorlevel%
)
