# Deployment Guide / Deployment-Anleitung

This guide explains how to create and publish releases of the File Organizer.

Diese Anleitung erklärt, wie du Releases des File Organizers erstellst und veröffentlichst.

## Recommended: GitHub Actions / Empfohlen: GitHub Actions

Releases are built on **Windows** in GitHub Actions. This is the recommended method — especially if you develop on Linux, where a local `.exe` build is not possible.

Releases werden auf **Windows** in GitHub Actions gebaut. Das ist die empfohlene Methode — besonders wenn du unter Linux entwickelst, wo kein lokaler `.exe`-Build möglich ist.

### Prerequisites / Voraussetzungen

- Changes pushed to the default branch / Änderungen auf den Default-Branch gepusht
- GitHub Actions enabled for the repository / GitHub Actions für das Repository aktiviert

### Create a release / Release erstellen

1. Open the repository on GitHub / Öffne das Repository auf GitHub
2. Go to **Actions** → **Release** / Gehe zu **Actions** → **Release**
3. Click **Run workflow** / Klicke auf **Run workflow**
4. Choose how to bump the version / Wähle, wie die Version erhöht werden soll:

| Option  | Example / Beispiel | When to use / Wann nutzen                          |
| ------- | ------------------ | -------------------------------------------------- |
| `patch` | 0.1.2 → 0.1.3      | Bug fixes / Bugfixes (default)                     |
| `minor` | 0.1.2 → 0.2.0      | New features / Neue Funktionen                     |
| `major` | 0.1.2 → 1.0.0      | Breaking changes / Breaking Changes                |
| `none`  | stays 0.1.2        | Re-build only, no version bump / Nur neu bauen     |

5. Click **Run workflow** / Klicke erneut auf **Run workflow**

### What the workflow does / Was der Workflow macht

1. Installs dependencies with `uv` / Installiert Abhängigkeiten mit `uv`
2. Compiles translations / Kompiliert Übersetzungen
3. Builds `FileOrganizer.exe` with PyInstaller / Baut `FileOrganizer.exe` mit PyInstaller
4. Creates `Release/FileOrganizer-{version}.zip` / Erstellt `Release/FileOrganizer-{version}.zip`
5. Commits the new `version.txt` (unless `none`) / Committet die neue `version.txt` (außer bei `none`)
6. Creates a GitHub Release with tag `v{version}` / Erstellt ein GitHub Release mit Tag `v{version}`

### After the workflow / Nach dem Workflow

If the version was bumped, pull the changes locally:

Wurde die Version erhöht, hole die Änderungen lokal ab:

```bash
git pull
```

The release appears under **Releases** on GitHub with the ZIP attached.

Das Release erscheint unter **Releases** auf GitHub mit dem ZIP als Download.

---

## Optional: Local build on Windows / Optional: Lokaler Build unter Windows

Only needed if you want to test the build process locally before triggering the workflow.

Nur nötig, wenn du den Build-Prozess lokal testen willst, bevor du den Workflow startest.

### Prerequisites / Voraussetzungen

- Windows
- Python 3.12 (not 3.14 — PyInstaller compatibility / nicht 3.14 — PyInstaller-Kompatibilität)
- [uv](https://github.com/astral-sh/uv) installed / installiert

### Steps / Schritte

```powershell
# Install dependencies / Abhängigkeiten installieren
uv sync

# Create release (interactive version prompt) / Release erstellen (interaktive Versionsabfrage)
uv run python scripts/create_release.py
```

Non-interactive options / Nicht-interaktive Optionen:

```powershell
uv run python scripts/create_release.py --bump patch
uv run python scripts/create_release.py --no-bump
```

Output / Ausgabe:

- `Release/FileOrganizer-{version}.zip`
- Build artifacts in `Release/files/` / Build-Artefakte in `Release/files/`

> **Note / Hinweis:** A local build does **not** create a GitHub Release. Upload the ZIP manually or use the GitHub Actions workflow instead.
>
> Ein lokaler Build erstellt **kein** GitHub Release. Lade das ZIP manuell hoch oder nutze stattdessen den GitHub-Actions-Workflow.

---

## Release package contents / Inhalt des Release-Pakets

```
Release/
├── FileOrganizer.exe
├── locales/
│   ├── de/
│   │   └── LC_MESSAGES/
│   │       └── messages.mo
│   └── en/
│       └── LC_MESSAGES/
│           └── messages.mo
└── README.txt
```

The ZIP file is named `FileOrganizer-{version}.zip` (e.g. `FileOrganizer-0.1.3.zip`).

Die ZIP-Datei heißt `FileOrganizer-{version}.zip` (z. B. `FileOrganizer-0.1.3.zip`).

## Version file / Versionsdatei

The current version is stored in `version.txt` at the project root.

Die aktuelle Version steht in `version.txt` im Projektroot.

The GitHub Actions workflow updates this file automatically when bumping the version.

Der GitHub-Actions-Workflow aktualisiert diese Datei automatisch, wenn die Version erhöht wird.

## Troubleshooting / Fehlerbehebung

| Problem                                              | Solution / Lösung                                                              |
| ---------------------------------------------------- | ------------------------------------------------------------------------------ |
| Workflow fails: tag already exists / Tag existiert   | Choose a version bump (`patch`, `minor`, `major`) instead of `none`           |
| Local build fails on Linux / Lokaler Build scheitert | Expected — use GitHub Actions / Erwartet — GitHub Actions nutzen               |
| Local build: `No module named 'pkg_resources'`     | Use Python 3.12, not 3.14 / Python 3.12 nutzen, nicht 3.14                    |
| `version.txt` out of sync / nicht synchron           | Run `git pull` after a successful workflow / Nach erfolgreichem Workflow `git pull` |
