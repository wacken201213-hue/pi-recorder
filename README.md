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

## 📋 Requirements
- Raspberry Pi (tested on Pi 3B+)
- 7" Touchscreen Display (800x480)
- Audio Hardware (USB microphone or audio interface)
- Video Hardware (USB Video Grabber for video recordings)

## 🛠️ Installation

### Quick Installation
```bash
git clone https://github.com/wacken201213-hue/pi-recorder.git
cd pi-recorder
chmod +x install.sh
./install.sh
```

### Manual Installation
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-tk ffmpeg alsa-utils

# Clone project
git clone https://github.com/wacken201213-hue/pi-recorder.git
cd pi-recorder

# Make start script executable
chmod +x pi-recorder.sh

# Desktop integration (optional)
cp pi-recorder.desktop ~/.local/share/applications/
```

## 🚀 Usage
```bash
./pi-recorder.sh
```

Or via Desktop Icon / Application Menu: **Audio/Video → Pi Recorder**

## 📱 Operation

### Main Menu
- **[Audio]** - Pure audio recording
- **[Video]** - Video recording with audio
- **[− Minimize]** - Minimize application
- **[× Exit]** - Close application

### Audio Recording
1. **[Start Recording]** → Enter filename → Recording starts
2. **Real-time Audio Level Meter** shows visual level feedback
3. **Duration Display** shows current recording time
4. **[Stop Recording]** → File saved

### Video Recording
1. **[Video Start]** → Enter filename → Recording starts  
2. **Duration Display** shows current recording time
3. **[Video Stop]** → File saved

### Keyboard Shortcuts
- **ESC** - Exit application
- **F11** - Toggle fullscreen

## ⚙️ Configuration

### Audio Devices
The application uses by default:
- **Audio Recording:** `plughw:1,0` (Card 1)
- **Video Audio:** `hw:2,0` (Video Grabber)

Test audio devices:
```bash
arecord -l  # List available devices
arecord -D plughw:1,0 -d 5 -f cd test.wav  # Test recording
```

### Video Settings
- **Format:** MP4 (H.264 + AAC)
- **Resolution:** 720x576, 25fps
- **Video Device:** `/dev/video0`

## 🎛️ Technical Details

### Audio Recording
- **Codec:** PCM 32-bit Little Endian
- **Sample Rate:** 44.1 kHz
- **Channels:** Stereo
- **Format:** WAV (uncompressed)
- **Audio Monitoring:** Real-time VU meter with color coding
  - Green: 0-50% (Normal level)
  - Yellow: 50-80% (High level)  
  - Red: 80-100% (Critical level)

### Video Recording
- **Video Codec:** libx264 (ultrafast preset)
- **Audio Codec:** AAC, 192 kbit/s
- **Container:** MP4

## 🔧 Troubleshooting

### Audio not working
```bash
# Check ALSA configuration
cat /proc/asound/cards

# Try different audio card
# In main.py: change "plughw:1,0" → "plughw:0,0"
```

### Video not working
```bash
# Check video devices
ls /dev/video*

# Test ffmpeg
ffmpeg -f v4l2 -i /dev/video0 -t 5 test.mp4
```

### Calibrate touchscreen
```bash
sudo apt install xinput-calibrator
xinput_calibrator
```

## 📁 Project Structure
```
pi-recorder/
├── main.py                 # Main application (Python/Tkinter)
├── pi-recorder.sh          # Start script
├── pi-recorder.desktop     # Desktop integration
├── pi-recorder-icon.png    # Application icon
├── install.sh              # Installation script
└── README.md              # This file
```

## 🤝 Contributing
Pull Requests and Issues are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

## 📝 License
This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments
- Developed for the Raspberry Pi Foundation
- Tested on Raspberry Pi 3B+ with official 7" touchscreen
- Uses ffmpeg for audio/video processing

---
**Developed for the Raspberry Pi Community 🥧❤️**