# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-08-29

### Added
- Real-time Audio Level Monitoring mit VU Meter
- Visuelle Pegelanzeige mit Farbkodierung (Grün/Gelb/Rot)
- Professional Audio Monitoring mit RMS-Berechnung
- 10Hz Update-Rate für flüssige Level-Anzeige
- Thread-basierte Audio-Level-Überwachung
- Automatisches Cleanup beim Beenden

### Changed
- Audio-Menü Layout erweitert für Level-Anzeige
- UI-Grid-Struktur angepasst (4 Reihen statt 3)
- Verbesserte Benutzeroberfläche für professionelle Anwendung

### Technical
- Neue Funktionen: `get_audio_level()`, `start_audio_level_monitoring()`, `stop_audio_level_monitoring()`
- Canvas-basierte VU-Meter Implementierung
- arecord Integration für Audio-Level-Monitoring
- Robuste Prozess-Verwaltung für Audio-Monitoring

## [1.0.0] - 2025-08-29

### Added
- Professionelle Audio-Aufnahme (WAV, 32-bit PCM, 44.1kHz)
- Video-Aufnahme mit Ton (MP4, H.264 + AAC)
- Touchscreen-optimierte Benutzeroberfläche (800x480)
- Vollbildmodus mit ESC-Taste zum Beenden
- Real-time Laufzeit-Anzeige
- ffmpeg-basierte Audio/Video-Verarbeitung
- ALSA Audio-System Integration
- Desktop-Integration (.desktop Datei)
- Automatisches Installationsskript
- Startscript mit Abhängigkeits-Prüfung

### Technical Details
- Python 3 + Tkinter GUI Framework
- Threading für nicht-blockierende Aufnahmen
- Subprocess-Management für ffmpeg
- Grid-basiertes responsives Layout
- Robuste Fehlerbehandlung

### Hardware Support
- Raspberry Pi 3B+ (getestet)
- 7" Touchscreen Display (800x480)
- USB Audio-Interfaces
- USB Video Grabber (Video-Aufnahme)
- ALSA-kompatible Audio-Geräte