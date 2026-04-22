@echo off
echo Cleaning build artifacts...

if exist build\ (
    rmdir /s /q build
    echo Deleted: build\
)

if exist dist\universal_downloader.exe (
    del /q dist\universal_downloader.exe
    echo Deleted: dist\universal_downloader.exe
)

if exist universal_downloader.spec (
    del /q universal_downloader.spec
    echo Deleted: universal_downloader.spec
)

echo Done.
