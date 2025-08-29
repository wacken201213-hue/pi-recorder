# Pi Recorder - Professional Audio & Video Recording Station

A professional-grade recording application designed for 7-inch touchscreens (800x480 resolution), featuring intuitive touch controls and real-time monitoring capabilities.

## ✨ Key Features

- **Dual Recording Modes**: High-quality audio (WAV) and video (MP4) recording
- **Real-time Audio Level Monitoring**: Professional VU meter with visual feedback
- **Touchscreen Optimized**: Large buttons and clear visual feedback for 800x480 displays
- **Professional Audio Quality**: 32-bit PCM, 44.1kHz stereo recording
- **HD Video Recording**: 720x576 resolution with H.264 encoding
- **Full-screen Operation**: Distraction-free recording environment
- **Hardware Integration**: ALSA audio system and V4L2 video capture
- **Real-time Duration Display**: Live recording time monitoring

![Pi Recorder Screenshot](screenshot.png)

## 📋 Voraussetzungen
- Raspberry Pi (getestet auf Pi 3B+)
- 7" Touchscreen Display (800x480)
- Audio-Hardware (USB-Mikrofon oder Audio-Interface)
- Video-Hardware (USB Video Grabber für Video-Aufnahmen)

## 🛠️ Installation

### Schnellinstallation
```bash
git clone https://github.com/wacken201213-hue/pi-recorder.git
cd pi-recorder
chmod +x install.sh
./install.sh
```

### Manuelle Installation
```bash
# Abhängigkeiten installieren
sudo apt update
sudo apt install python3 python3-tk ffmpeg alsa-utils

# Projekt clonen
git clone https://github.com/wacken201213-hue/pi-recorder.git
cd pi-recorder

# Startscript ausführbar machen
chmod +x pi-recorder.sh

# Desktop-Integration (optional)
cp pi-recorder.desktop ~/.local/share/applications/
```

## 🚀 Starten
```bash
./pi-recorder.sh
```

Oder über das Desktop-Icon / Anwendungsmenü: **Audio/Video → Pi Recorder**

## 📱 Bedienung

### Hauptmenü
- **[Audio]** - Reine Audio-Aufnahme
- **[Video]** - Video-Aufnahme mit Ton
- **[− Minimieren]** - Anwendung minimieren
- **[× Beenden]** - Anwendung schließen

### Audio-Aufnahme
1. **[Aufnahme starten]** → Dateiname eingeben → Aufnahme läuft
2. **Real-time Audio Level Meter** zeigt visuellen Pegel an
3. **Laufzeit-Anzeige** zeigt aktuelle Zeit
4. **[Aufnahme stoppen]** → Datei gespeichert

### Video-Aufnahme
1. **[Video Start]** → Dateiname eingeben → Aufnahme läuft  
2. **Laufzeit-Anzeige** zeigt aktuelle Zeit
3. **[Video Stop]** → Datei gespeichert

### Tastenkürzel
- **ESC** - App beenden
- **F11** - Vollbild ein/aus

## ⚙️ Konfiguration

### Audio-Geräte
Die Anwendung verwendet standardmäßig:
- **Audio-Aufnahme:** `plughw:1,0` (Card 1)
- **Video-Audio:** `hw:2,0` (Video Grabber)

Audio-Geräte testen:
```bash
arecord -l  # Verfügbare Geräte anzeigen
arecord -D plughw:1,0 -d 5 -f cd test.wav  # Test-Aufnahme
```

### Video-Einstellungen
- **Format:** MP4 (H.264 + AAC)
- **Auflösung:** 720x576, 25fps
- **Video-Gerät:** `/dev/video0`

## 🎛️ Technische Details

### Audio-Aufnahme
- **Codec:** PCM 32-bit Little Endian
- **Samplerate:** 44.1 kHz
- **Kanäle:** Stereo
- **Format:** WAV (unkomprimiert)
- **Audio-Monitoring:** Real-time VU meter mit Farbkodierung
  - Grün: 0-50% (Normaler Pegel)
  - Gelb: 50-80% (Hoher Pegel)  
  - Rot: 80-100% (Kritischer Pegel)

### Video-Aufnahme
- **Video-Codec:** libx264 (ultrafast preset)
- **Audio-Codec:** AAC, 192 kbit/s
- **Container:** MP4

## 🔧 Problembehandlung

### Audio funktioniert nicht
```bash
# ALSA-Konfiguration prüfen
cat /proc/asound/cards

# Andere Audio-Karte versuchen
# In main.py: "plughw:1,0" → "plughw:0,0"
```

### Video funktioniert nicht
```bash
# Video-Geräte prüfen
ls /dev/video*

# ffmpeg-Test
ffmpeg -f v4l2 -i /dev/video0 -t 5 test.mp4
```

### Touchscreen kalibrieren
```bash
sudo apt install xinput-calibrator
xinput_calibrator
```

## 📁 Projektstruktur
```
pi-recorder/
├── main.py                 # Hauptanwendung (Python/Tkinter)
├── pi-recorder.sh          # Startscript
├── pi-recorder.desktop     # Desktop-Integration
├── pi-recorder-icon.png    # Anwendungs-Icon
├── install.sh              # Installationsskript
└── README.md              # Diese Datei
```

## 🤝 Beitragen
Pull Requests und Issues sind willkommen!

1. Repository forken
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'Add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request erstellen

## 📝 Lizenz
Dieses Projekt steht unter der [MIT License](LICENSE).

## 🙏 Danksagungen
- Entwickelt für Raspberry Pi Foundation
- Getestet auf Raspberry Pi 3B+ mit offiziellem 7" Touchscreen
- Verwendet ffmpeg für Audio/Video-Verarbeitung

---
**Entwickelt für die Raspberry Pi Community 🥧❤️**