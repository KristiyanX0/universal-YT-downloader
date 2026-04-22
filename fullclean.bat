@echo off
echo Running full clean...

call clean.bat

if exist env\ (
    rmdir /s /q env
    echo Deleted: env\
)

echo Full clean done.
