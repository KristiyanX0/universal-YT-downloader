@echo off
echo Setting up environment...

:: Create virtual environment
if not exist env (
    python3 -m venv env
    if not exist env\Scripts\activate.bat (
        echo ERROR: Failed to create virtual environment. Make sure Python is installed correctly.
        exit /b 1
    )
    echo Created virtual environment: env\
) else (
    echo Virtual environment already exists, skipping.
)

:: Activate and install packages
call env\Scripts\activate.bat

echo Installing required packages...
env\Scripts\pip install yt-dlp rich pyinstaller

echo.
echo Setup complete! To activate the environment run:
echo     env\Scripts\activate.bat
