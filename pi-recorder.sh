#!/bin/bash

# Pi Recorder Startscript
# Starte die Pi Recorder Anwendung im Vollbildmodus

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Prüfe ob Python 3 verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "Fehler: Python 3 ist nicht installiert!"
    echo "Installation: sudo apt install python3 python3-tk"
    exit 1
fi

# Prüfe ob tkinter verfügbar ist
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "Fehler: tkinter ist nicht installiert!"
    echo "Installation: sudo apt install python3-tk"
    exit 1
fi

# Prüfe ob ffmpeg verfügbar ist
if ! command -v ffmpeg &> /dev/null; then
    echo "Fehler: ffmpeg ist nicht installiert!"
    echo "Installation: sudo apt install ffmpeg"
    exit 1
fi

echo "Starte Pi Recorder..."
python3 main.py