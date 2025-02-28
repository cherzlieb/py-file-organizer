# Translation Guide / Übersetzungsanleitung

This document explains how to create and update translations for the File Organizer.

## Directory Structure / Verzeichnisstruktur

```
src/
└── locales/
    ├── de/
    │   └── LC_MESSAGES/
    │       ├── messages.po   # German translations
    │       └── messages.mo   # Compiled German translations
    └── en/
        └── LC_MESSAGES/
            ├── messages.po   # English translations
            └── messages.mo   # Compiled English translations
```

## Creating New Translations / Neue Übersetzungen erstellen

1. Create a new `.po` file / Neue `.po` Datei erstellen:

```bash
mkdir -p src/locales/<language_code>/LC_MESSAGES
touch src/locales/<language_code>/LC_MESSAGES/messages.po
```

2. Add header information / Header-Informationen hinzufügen:

```po
msgid ""
msgstr ""
"Project-Id-Version: File Organizer 1.0\n"
"POT-Creation-Date: 2024-02-27 12:00+0100\n"
"PO-Revision-Date: 2024-02-27 12:00+0100\n"
"Last-Translator: Your Name\n"
"Language-Team: Language\n"
"Language: <language_code>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
```

3. Add translations / Übersetzungen hinzufügen:

```po
msgid "Original Text"
msgstr "Translated Text"
```

## Compiling Translations / Übersetzungen kompilieren

Run the compile script / Kompilierungsskript ausführen:

```bash
python scripts/compile_translations.py
```

## Adding New Strings / Neue Texte hinzufügen

1. Mark strings in code / Texte im Code markieren:

```python
from gettext import gettext as _
text = _("Text to translate")
```

2. Add translations to `.po` files / Übersetzungen in `.po` Dateien hinzufügen:

```po
msgid "Text to translate"
msgstr "Übersetzter Text"
```

3. Recompile translations / Übersetzungen neu kompilieren

## Testing Translations / Übersetzungen testen

Run the test script / Testskript ausführen:

```bash
python scripts/test_translations.py
```

## Common Issues / Häufige Probleme

-   **Missing .mo files**: Run compile script / Kompilierungsskript ausführen
-   **Translation not showing**: Check if string is marked with `_()` / Prüfen ob Text mit `_()` markiert ist
-   **Wrong encoding**: Ensure UTF-8 encoding / UTF-8-Kodierung sicherstellen
