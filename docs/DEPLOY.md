# Deployment Guide / Deployment-Anleitung

This guide explains how to create and deploy releases of the File Organizer.

## Prerequisites / Voraussetzungen

- Python 3.12 or later / Python 3.12 oder höher
- Virtual environment / Virtuelle Umgebung
- PyInstaller / PyInstaller

## Build Release / Release erstellen

1. Prepare environment / Umgebung vorbereiten:
```bash
# Activate virtual environment / Virtuelle Umgebung aktivieren
.\venv\Scripts\activate

# Install dependencies / Abhängigkeiten installieren
pip install -r requirements.txt
```

2. Create release / Release erstellen:
```bash
python scripts/create_release.py
```

The script will create / Das Skript erstellt:
- `FileOrganizer-v1.0.0.zip` in the root directory / im Hauptverzeichnis
- Release files in the `Release` folder / Release-Dateien im `Release`-Ordner

## Directory Structure / Verzeichnisstruktur

```
Release/
├── FileOrganizer.exe
├── config/
│   └── .env
├── locales/
│   ├── de/
│   │   └── LC_MESSAGES/
│   │       └── messages.mo
│   └── en/
│       └── LC_MESSAGES/
│           └── messages.mo
└── README.txt
```

## GitHub Release / GitHub-Release

1. Tag version / Version taggen:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

2. Create GitHub Release / GitHub-Release erstellen:
- Go to GitHub Releases / Gehe zu GitHub Releases
- Click "Draft a new release" / Klicke auf "Draft a new release"
- Select tag "v1.0.0" / Wähle Tag "v1.0.0"
- Title: "File Organizer v1.0.0" / Titel: "File Organizer v1.0.0"
- Upload `FileOrganizer-v1.0.0.zip` / Lade `FileOrganizer-v1.0.0.zip` hoch
- Click "Publish release" / Klicke auf "Publish release"