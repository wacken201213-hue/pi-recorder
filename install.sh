#!/bin/bash

# Pi Recorder Installation Script
# Installiert alle Abhängigkeiten und richtet das System ein

echo "=== Pi Recorder Installation ==="
echo

# Prüfe ob als root ausgeführt wird
if [[ $EUID -eq 0 ]]; then
   echo "Dieses Script sollte NICHT als root ausgeführt werden!"
   echo "Führe es als normaler Benutzer aus."
   exit 1
fi

# System aktualisieren
echo "[1/6] Aktualisiere Pakete..."
sudo apt update

# Abhängigkeiten installieren
echo "[2/6] Installiere Abhängigkeiten..."
sudo apt install -y python3 python3-tk ffmpeg alsa-utils

# Prüfe Installation
echo "[3/6] Prüfe Installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Fehler: Python 3 Installation fehlgeschlagen!"
    exit 1
fi

if ! python3 -c "import tkinter" &> /dev/null; then
    echo "❌ Fehler: tkinter Installation fehlgeschlagen!"
    exit 1
fi

if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Fehler: ffmpeg Installation fehlgeschlagen!"
    exit 1
fi

echo "✅ Alle Abhängigkeiten erfolgreich installiert!"

# Skripte ausführbar machen
echo "[4/6] Mache Skripte ausführbar..."
chmod +x pi-recorder.sh

# Desktop-Integration
echo "[5/6] Installiere Desktop-Integration..."
mkdir -p ~/.local/share/applications
cp pi-recorder.desktop ~/.local/share/applications/

# Pfade in .desktop-Datei anpassen
CURRENT_DIR=$(pwd)
sed -i "s|/home/pi/pi-recorder|$CURRENT_DIR|g" ~/.local/share/applications/pi-recorder.desktop

echo "[6/6] Installation abgeschlossen!"
echo
echo "=== Pi Recorder wurde erfolgreich installiert! ==="
echo
echo "Starten:"
echo "  Kommandozeile: ./pi-recorder.sh"
echo "  Desktop:       Anwendungsmenü > Audio/Video > Pi Recorder"
echo
echo "Erste Schritte:"
echo "  1. Audio-Gerät testen:  arecord -l"
echo "  2. Video-Gerät testen:  ls /dev/video*"
echo "  3. Anwendung starten:   ./pi-recorder.sh"
echo
echo "Bei Problemen siehe: https://github.com/wacken201213-hue/pi-recorder#troubleshooting"
echo