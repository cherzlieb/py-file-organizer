# Datei-Organisierer

Dieses Projekt ist eine einfache Python-Anwendung, die Dateien in Ihrem Downloads-Ordner automatisch sortiert, indem sie diese basierend auf ihren Dateitypen in separate Ordner einordnet. Dies hilft dabei, Ihren Downloads-Ordner übersichtlich zu halten und macht es einfacher, Dateien wiederzufinden.

## Funktionen

-   Automatische Sortierung von Dateien in entsprechende Ordner basierend auf ihren Typen (z.B. Bilder, Musik, Dokumente)
-   Unterstützung verschiedener Dateitypen wie Bilder, Audio-Dateien, Dokumente und mehr
-   Automatisches Hinzufügen des Erstellungsdatums zum Dateinamen
-   Verschieben von Ordnern in einen "Unorganized"-Ordner
-   Bereinigung von Dateinamen (Ersetzung von Leerzeichen und Unterstrichen durch Bindestriche)

## Projektstruktur

```
file-organizer
├── src
│   ├── main.py          # Hauptprogramm
│   └── utils
│       ├── file_utils.py # Hilfsfunktionen für die Dateiverwaltung
│       └── file_types.py # Definition der Dateitypen
├── requirements.txt     # Abhängigkeiten
└── README.md           # Projektdokumentation
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

## Verwendung

1. Öffnen Sie die Datei `src/main.py` und passen Sie den Pfad zu Ihrem Downloads-Ordner an:

    ```python
    DOWNLOADS_FOLDER = "E:/Downloads"  # Ändern Sie dies zu Ihrem Downloads-Pfad
    ```

2. Führen Sie das Programm aus:
    ```
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
