# Datei-Organisierer

Dieses Projekt ist eine einfache Python-Anwendung, die Dateien in Ihrem Downloads-Ordner automatisch sortiert, indem sie diese basierend auf ihren Dateitypen in separate Ordner einordnet. Dies hilft dabei, Ihren Downloads-Ordner übersichtlich zu halten und macht es einfacher, Dateien wiederzufinden.

## Funktionen

-   Automatische Sortierung von Dateien in entsprechende Ordner basierend auf ihren Typen
-   Unterstützung verschiedener Dateitypen
-   Automatisches Hinzufügen des Änderungs- oder Erstellungsdatums zum Dateinamen (konfigurierbar)
-   Verschieben von Ordnern in einen "Unorganized"-Ordner
-   Bereinigung von Dateinamen
-   Konfiguration über .env Datei
-   Ausführliches Logging

## Projektstruktur

```path
file-organizer/
├── src/
│   ├── main.py                 # Hauptprogramm
│   ├── config.py               # Konfigurationsklassen
│   └── utils/
│       ├── file_utils.py       # Hauptlogik für Dateiorganisation
│       ├── file_types.py       # Definition der Dateitypen
│       ├── file_operations.py  # Dateioperationen
│       ├── date_utils.py       # Datumsfunktionen
│       ├── path_utils.py       # Pfadoperationen
│       └── filename_utils.py   # Dateinamenverarbeitung
├── logs/                       # Logdateien (wird automatisch erstellt)
├── .env.example                # Beispiel-Umgebungsvariablen
├── requirements.txt            # Python-Abhängigkeiten
└── README.md                   # Projektdokumentation
```

## Voraussetzungen

Um dieses Projekt ausführen zu können, benötigen Sie Python auf Ihrem Computer. Zusätzliche Abhängigkeiten sind in der `requirements.txt` aufgeführt.

## Installation

1. Klonen Sie das Repository auf Ihren lokalen Computer:

    ```bash
    git clone https://github.com/cherzlieb/py-file-organizer
    ```

2. Wechseln Sie in das Projektverzeichnis:

    ```bash
    cd file-organizer
    ```

3. Erstellen Sie eine virtuelle Umgebung:

    ```bash
    python -m venv venv
    ```

4. Aktivieren Sie die virtuelle Umgebung:

    ```bash
    # Windows
    .\venv\Scripts\activate

    # Linux/Mac
    source venv/bin/activate
    ```

5. Installieren Sie die erforderlichen Abhängigkeiten:

    ```bash
    pip install -r requirements.txt
    ```

## Konfiguration

1. Kopieren Sie die `.env.example` Datei zu `.env`:

    ```bash
    cp .env.example .env
    ```

2. Passen Sie die Pfade in der [.env](http://_vscodecontentref_/12) Datei an:

    ```ini
    SOURCE_FOLDER = ""      # Hier den Pfad angeben, welcher sortiert werden soll.
    ORGANIZED_FOLDER = ""   # Hier den Pfad angeben, wohin die sortierten Dateien sollen (in dem Unterordner Organized).
    UNORGANIZED_FOLDER = "" # Hier den Pfad angeben, wohin die unsortierten Ordner sollen (in dem Unterordner Unorganized).
    LOG_FILE = ""           # Pfad zur Log-Datei, sowie der Name (liegt im Projekt-Ordner)
    DEBUG = False           # Hier angeben ob der Debug Modus aktiviert werden soll.
    ```

## Verwendung

Führen Sie das Programm aus:

```bash
python src/main.py
```

Das Programm wird:

-   Dateien nach Typ sortieren und in entsprechende Unterordner verschieben
-   Dem Dateinamen das Erstellungsdatum voranstellen
-   Ordner in einen "Unorganized"-Ordner verschieben
-   Den Fortschritt in der Konsole anzeigen

## Mitwirken

Beiträge sind willkommen! Wenn Sie Vorschläge für Verbesserungen oder neue Funktionen haben, können Sie gerne ein Issue eröffnen oder einen Pull Request einreichen.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Details finden Sie in der LICENSE-Datei.

## Änderungen

Die wichtigsten Änderungen sind:

-   Aktualisierte Projektstruktur
-   Neue Konfigurationsmethode über `.env`
-   Präzisere Beschreibung der Datumsfunktionalität
-   Hinzufügung der neuen Logging-Funktion
-   Entfernung der veralteten `DOWNLOADS_FOLDER` Referenz
-   Genauere Beschreibung der Modulstruktur
