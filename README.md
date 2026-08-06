# Datei-Organisierer / File Organizer

[![Release](https://img.shields.io/github/v/release/cherzlieb/py-file-organizer)](https://github.com/cherzlieb/py-file-organizer/releases)

Dieses Projekt ist eine Python-Anwendung mit grafischer Benutzeroberfläche, die Dateien automatisch basierend auf ihren Dateitypen sortiert. Die Anwendung unterstützt mehrere Sprachen und bietet umfangreiche Konfigurationsmöglichkeiten.

This is a Python application with a graphical user interface that automatically organizes files based on their types. The application supports multiple languages and offers extensive configuration options.

## Hauptfunktionen / Main Features

- 🌍 Mehrsprachig (Deutsch/Englisch) / Multilingual (German/English)
- 🖥️ Grafische Benutzeroberfläche / Graphical User Interface
- 📂 Automatische Dateisortierung / Automatic File Sorting
- 📅 Datums-basierte Organisierung / Date-based Organization
- 🔍 Debug-Modus mit Logging / Debug Mode with Logging
- ⚙️ Konfigurationsspeicherung / Configuration Saving

## Sprachen / Languages

Ausführliche Dokumentation ist verfügbar in: / Detailed documentation is available in:

- [Deutsch (German)](docs/README_de.md)
- [English](docs/README_en.md)

## Quick Start / Schnellstart

1. Repository klonen / Clone repository:

```bash
git clone [https://github.com/cherzlieb/py-file-organizer](https://github.com/cherzlieb/py-file-organizer)
cd py-file-organizer
```

Wählen Sie eine der folgenden Installationsmethoden: / Choose one of the following installation methods:

### Option A: Mit `uv` (Empfohlen / Recommended)

[uv](https://github.com/astral-sh/uv) ist ein extrem schneller Python-Paketmanager.

```bash
# Umgebung einrichten & Abhängigkeiten installieren / Setup environment & install dependencies
uv sync

# Übersetzungen kompilieren / Compile translations
uv run python scripts/compile_translations.py

# Anwendung starten / Launch application
uv run python src/main.py
```

### Option B: Klassische Methode / Classical Method (`venv` & `pip`)

1. Virtuelle Umgebung erstellen / Create virtual environment:

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

2. Abhängigkeiten installieren / Install dependencies:

```bash
pip install -r requirements.txt
```

3. Übersetzungen kompilieren / Compile translations:

```bash
python scripts/compile_translations.py
```

4. Starten Sie die Anwendung / Launch the application:

```bash
python src/main.py
```

---

## Erste Schritte / First Steps

1. Wählen Sie Ihre Sprache / Select your language
2. Konfigurieren Sie die Ordner / Configure folders:
* Quellordner / Source folder
* Zielordner / Target folder
* Nicht-sortierbare / Unorganized


3. Klicken Sie auf "Start" / Click "Start"

## Screenshots

### Englisch / English

### Deutsch / German

## Development / Entwicklung

For build and deployment instructions, see [DEPLOY.md](https://www.google.com/search?q=docs/DEPLOY.md).

Informationen zum Erstellen und Veröffentlichen finden Sie in der [DEPLOY.md](https://www.google.com/search?q=docs/DEPLOY.md).
