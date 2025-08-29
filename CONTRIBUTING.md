# Beitragen zu Pi Recorder

Vielen Dank für dein Interesse, zu Pi Recorder beizutragen! 🎉

## 🚀 Wie kann ich beitragen?

### Bug Reports
- Verwende die [GitHub Issues](https://github.com/wacken201213-hue/pi-recorder/issues)
- Beschreibe das Problem detailliert
- Füge System-Informationen hinzu (Pi-Modell, OS-Version)
- Stelle Logs/Fehlermeldungen bereit

### Feature Requests
- Erstelle ein GitHub Issue mit dem Label "enhancement"
- Erkläre den Use Case und Nutzen
- Skizziere mögliche Implementierung

### Code Contributions
1. **Fork** das Repository
2. Erstelle einen **Feature Branch** (`git checkout -b feature/amazing-feature`)
3. **Committe** deine Änderungen (`git commit -m 'Add amazing feature'`)
4. **Push** zum Branch (`git push origin feature/amazing-feature`)
5. Erstelle einen **Pull Request**

## 🛠️ Entwicklung

### Setup
```bash
git clone https://github.com/wacken201213-hue/pi-recorder.git
cd pi-recorder
./install.sh
```

### Testing
```bash
# Lokaler Test
python3 main.py

# Audio-Test
arecord -l
arecord -D plughw:1,0 -d 5 -f cd test.wav

# Video-Test
ls /dev/video*
ffmpeg -f v4l2 -i /dev/video0 -t 5 test.mp4
```

### Code Style
- Python PEP 8 Style Guide befolgen
- Aussagekräftige Variablen- und Funktionsnamen
- Deutsche Kommentare für UI/UX, englische für technische Details
- Threading sauber implementieren (daemon=True)
- Robuste Fehlerbehandlung

## 🎯 Prioritäten

### Hochpriorität
- Performance-Optimierungen
- Bessere Fehlerbehandlung
- Hardware-Kompatibilität erweitern
- Touchscreen-Usability verbessern

### Gewünschte Features
- Multi-Track Audio-Aufnahme
- Audio-Effects/Filter
- Aufnahme-Presets
- Batch-Export Funktionen
- Konfigurationsdatei-Support
- Automatische Hardware-Erkennung

### Technische Verbesserungen
- Unit Tests hinzufügen
- CI/CD Pipeline
- Packaging (deb/rpm)
- Logging-System
- Konfigurationsmanagement

## 📋 Pull Request Guidelines

### Checkliste
- [ ] Code folgt Style Guidelines
- [ ] Neue Features sind dokumentiert
- [ ] Tests wurden durchgeführt
- [ ] Commit-Messages sind aussagekräftig
- [ ] README.md wurde aktualisiert (falls nötig)
- [ ] CHANGELOG.md wurde erweitert

### Commit Messages
```
Type: Brief description

Detailed explanation of the changes.
Why was this change made?
What does it solve?

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🤝 Community Guidelines

- Sei respektvoll und konstruktiv
- Hilf anderen Entwicklern
- Dokumentiere deine Änderungen
- Teste auf echter Hardware wenn möglich
- Berücksichtige verschiedene Pi-Modelle

## 📞 Kontakt

- GitHub Issues für Bugs/Features
- Discussions für allgemeine Fragen
- Pull Requests für Code-Beiträge

---

**Vielen Dank für deinen Beitrag zur Raspberry Pi Community! 🥧❤️**