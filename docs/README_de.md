# Datei-Organisierer

Dieses Projekt ist eine einfache Python-Anwendung, die Dateien in Ihrem Downloads-Ordner automatisch sortiert, indem sie diese basierend auf ihren Dateitypen in separate Ordner einordnet. Dies hilft dabei, Ihren Downloads-Ordner übersichtlich zu halten und macht es einfacher, Dateien wiederzufinden.

## Funktionen

- Automatische Sortierung von Dateien in entsprechende Ordner basierend auf ihren Typen
- Unterstützung verschiedener Dateitypen
- Automatisches Hinzufügen des Änderungs- oder Erstellungsdatums zum Dateinamen (konfigurierbar)
- Verschieben von Ordnern in einen "Unorganized"-Ordner
- Bereinigung von Dateinamen
- Konfiguration über .env Datei
- Ausführliches Logging
- Grafische Benutzeroberfläche (GUI)
- Mehrsprachenunterstützung (Deutsch/Englisch)

## Projektstruktur

```path
file-organizer/
├── src/
│   ├── core/
│   │   ├── config.py           # Konfigurationsklassen
│   │   ├── constants.py        # Konstanten
│   │   └── translation.py      # Übersetzungsfunktionen
│   ├── gui/
│   │   ├── components.py       # GUI-Komponenten
│   │   ├── config_handler.py   # Konfigurationsverwaltung
│   │   └── main_window.py      # Hauptfenster
│   ├── utils/                  # Hilfsfunktionen
│   │   ├── file_types.py       # Dateityp-Definitionen
│   │   └── file_utils.py       # Dateioperationen
│   └── main.py                 # Hauptprogramm
├── locales/                    # Sprachdateien
│   ├── de/                     # Deutsche Übersetzungen
│   └── en/                     # Englische Übersetzungen
├── logs/                       # Logdateien
└── README.md                   # Dokumentation
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

Die Konfiguration kann über die grafische Benutzeroberfläche oder die `.env` Datei erfolgen.

### Über die GUI (empfohlen)

Starten Sie das Programm und konfigurieren Sie die Einstellungen im Hauptfenster:

1. Wählen Sie die gewünschte Sprache (Deutsch/Englisch)
2. Geben Sie die Ordnerpfade an:
   - Quellordner: Der zu organisierende Ordner
   - Zielordner: Ordner für sortierte Dateien
   - Nicht-sortierbare: Ordner für nicht sortierbare Elemente
3. Aktivieren Sie optional:
   - Debug-Modus für detaillierte Protokollierung
   - Erstellungsdatum verwenden
   - Datum erzwingen
   - Datum zu Ordnern hinzufügen
4. Klicken Sie auf "Konfiguration speichern"

Die Einstellungen werden automatisch in der `.env` Datei gespeichert.

### Manuelle Konfiguration (alternativ)

Alternativ können Sie die `.env` Datei direkt bearbeiten:

```ini
SOURCE_FOLDER=""         # Quellordner
ORGANIZED_FOLDER=""      # Zielordner für sortierte Dateien
UNORGANIZED_FOLDER=""    # Ordner für nicht sortierbare Elemente
LOG_FILE=""             # Pfad zur Log-Datei
DEBUG=False             # Debug-Modus (True/False)
USE_CREATION_DATE=False # Erstellungsdatum verwenden (True/False)
FORCE_DATE=False        # Datum erzwingen (True/False)
DATE_FOLDERS=False      # Datum zu Ordnern hinzufügen (True/False)
LANGUAGE="de"           # Sprache (de/en)
```

## Verwendung

Führen Sie das Programm aus:

```bash
python src/main.py
```

### Grafische Benutzeroberfläche (GUI)

Nach dem Start des Programms erscheint das Hauptfenster mit folgenden Optionen:

- **Sprache**: Wählen Sie zwischen Deutsch und Englisch
- **Quellordner**: Der zu organisierende Ordner
- **Zielordner**: Ordner für sortierte Dateien
- **Nicht-sortierbare**: Ordner für nicht sortierbare Elemente
- **Debug-Modus**: Aktiviert detaillierte Protokollierung
- **Erstellungsdatum verwenden**: Nutzt das Erstellungsdatum statt Änderungsdatum
- **Datum erzwingen**: Fügt immer ein Datum hinzu
- **Datum zu Ordnern**: Fügt auch Ordnern ein Datum hinzu

Die Einstellungen werden automatisch gespeichert und beim nächsten Start wiederhergestellt.

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
