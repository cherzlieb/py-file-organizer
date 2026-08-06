# Deployment Guide / Deployment-Anleitung

This guide explains how to create and publish releases of the File Organizer.

Diese Anleitung erklärt, wie du Releases des File Organizers erstellst und veröffentlichst.

## Recommended: GitHub Actions / Empfohlen: GitHub Actions

Releases are built on **Windows** in GitHub Actions and triggered by pushing a **git tag**.

Releases werden auf **Windows** in GitHub Actions gebaut und durch das Pushen eines **Git-Tags** ausgelöst.

### Create a release / Release erstellen

1. Make sure your changes are merged on `main` / Stelle sicher, dass deine Änderungen auf `main` sind
2. Create and push a version tag / Erstelle und pushe einen Versions-Tag:

```bash
git tag v0.2.0
git push origin v0.2.0
```

The tag name defines the release version. Prefix `v` is optional in the build script but recommended for GitHub.

Der Tag-Name bestimmt die Release-Version. Das Präfix `v` ist im Build-Skript optional, für GitHub aber empfohlen.

3. The **Release** workflow starts automatically / Der **Release**-Workflow startet automatisch
4. When finished, download the ZIP under **Releases** / Nach Abschluss das ZIP unter **Releases** herunterladen

### What the workflow does / Was der Workflow macht

1. Reads the version from the pushed tag (e.g. `v0.2.0` → `0.2.0`) / Liest die Version aus dem gepushten Tag
2. Installs dependencies with `uv` / Installiert Abhängigkeiten mit `uv`
3. Compiles translations / Kompiliert Übersetzungen
4. Builds `FileOrganizer.exe` with PyInstaller / Baut `FileOrganizer.exe` mit PyInstaller
5. Creates `Release/FileOrganizer-{version}.zip` / Erstellt `Release/FileOrganizer-{version}.zip`
6. Publishes a GitHub Release for the tag / Veröffentlicht ein GitHub Release für den Tag

### Versioning / Versionierung

There is no separate `version.txt`. The git tag is the single source of truth.

Es gibt keine separate `version.txt`. Der Git-Tag ist die einzige Versionsquelle.

Examples / Beispiele:

| Tag       | ZIP name                      | GitHub Release   |
| --------- | ----------------------------- | ---------------- |
| `v0.2.0`  | `FileOrganizer-0.2.0.zip`     | `File Organizer v0.2.0` |
| `v1.0.0`  | `FileOrganizer-1.0.0.zip`     | `File Organizer v1.0.0` |

---

## Optional: Local build on Windows / Optional: Lokaler Build unter Windows

Only needed if you want to test the build process locally before creating a tag.

Nur nötig, wenn du den Build-Prozess lokal testen willst, bevor du einen Tag erstellst.

### Prerequisites / Voraussetzungen

- Windows
- Python 3.12 (not 3.14 — PyInstaller compatibility / nicht 3.14 — PyInstaller-Kompatibilität)
- [uv](https://github.com/astral-sh/uv) installed / installiert

### Steps / Schritte

```powershell
# Install dependencies / Abhängigkeiten installieren
uv sync

# Build using the latest git tag / Build mit dem neuesten Git-Tag
uv run python scripts/create_release.py

# Or specify a version explicitly / Oder Version explizit angeben
uv run python scripts/create_release.py --version 0.2.0
```

Output / Ausgabe:

- `Release/FileOrganizer-{version}.zip`
- Build artifacts in `Release/files/` / Build-Artefakte in `Release/files/`

> **Note / Hinweis:** A local build does **not** create a GitHub Release. Push a tag or upload the ZIP manually.
>
> Ein lokaler Build erstellt **kein** GitHub Release. Tag pushen oder ZIP manuell hochladen.

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

## Troubleshooting / Fehlerbehebung

| Problem                                              | Solution / Lösung                                                              |
| ---------------------------------------------------- | ------------------------------------------------------------------------------ |
| Workflow does not start / startet nicht              | Tag must match `v*` (e.g. `v0.2.0`) / Tag muss `v*` entsprechen (z. B. `v0.2.0`) |
| Workflow fails: tag/release already exists / existiert | Delete tag and release on GitHub, then re-push / Tag und Release auf GitHub löschen, erneut pushen |
| Local build fails on Linux / Lokaler Build scheitert | Expected — use GitHub Actions / Erwartet — GitHub Actions nutzen               |
| Local build: `No module named 'pkg_resources'`     | Fixed by `altgraph>=0.17.5` (works with `setuptools>=82`) / Behoben durch `altgraph>=0.17.5` |
| Local build: no git tag / kein Git-Tag               | Create a tag first or pass `--version` / Tag erstellen oder `--version` angeben |
