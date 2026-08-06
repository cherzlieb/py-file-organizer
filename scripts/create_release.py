import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from clear_release_by_error import main as clear_release_by_error


def parse_args():
    parser = argparse.ArgumentParser(description="Create a release package.")
    parser.add_argument(
        "--version",
        help="Release version (e.g. 0.2.0). Defaults to the latest git tag.",
    )
    return parser.parse_args()


def resolve_version(version: str | None) -> str:
    if version:
        return version.lstrip("v")

    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().lstrip("v")


def create_release(version: str | None = None):
    """Create a release package."""
    try:
        compile_script = Path(__file__).parent / "compile_translations.py"
        print(f"Compiling translations using: {compile_script}")
        subprocess.run([sys.executable, str(compile_script)], check=True)

        root_dir = Path(__file__).parent.parent
        release_dir = root_dir / "Release"
        dist_dir = root_dir / "dist"
        current_version = resolve_version(version)
        zip_name = f"FileOrganizer-{current_version}"

        print(f"Creating release v{current_version} in: {release_dir}")

        if release_dir.exists():
            shutil.rmtree(release_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)

        (release_dir / "locales/de/LC_MESSAGES").mkdir(parents=True)
        (release_dir / "locales/en/LC_MESSAGES").mkdir(parents=True)

        build_script = root_dir / "scripts" / "build_exe.py"
        print(f"Building executable using: {build_script}")
        subprocess.run([sys.executable, str(build_script)], check=True)

        if dist_dir.exists() and (dist_dir / "FileOrganizer.exe").exists():
            print("Copying files to release directory...")
            shutil.copy2(dist_dir / "FileOrganizer.exe", release_dir)

            for lang in ["de", "en"]:
                src_mo = root_dir / f"src/locales/{lang}/LC_MESSAGES/messages.mo"
                dst_mo = release_dir / f"locales/{lang}/LC_MESSAGES/messages.mo"
                if src_mo.exists():
                    shutil.copy2(src_mo, dst_mo)
                else:
                    print(f"Warning: Translation file not found: {src_mo}")

            with open(release_dir / "README.txt", "w", encoding="utf-8") as f:
                f.write(f"""File Organizer v{current_version}

1. Erste Schritte / First Steps:
   - Starten Sie FileOrganizer.exe / Start FileOrganizer.exe
   - Wählen Sie Ihre Sprache / Select your language
   - Konfigurieren Sie die Ordnerpfade / Configure folder paths
   - Konfigurationsdatei unter: / Configuration file at: config/.env

2. Unterstützte Sprachen / Supported Languages:
   - Deutsch / German
   - Englisch / English

Bei Problemen besuchen Sie / For issues visit:
https://github.com/cherzlieb/py-file-organizer""")

            zip_path = release_dir / f"{zip_name}.zip"
            print(f"Creating ZIP file: {zip_path}")

            release_files_dir = release_dir / "files"

            if release_files_dir.exists():
                shutil.rmtree(release_files_dir)
            release_files_dir.mkdir()

            for item in release_dir.iterdir():
                if item != release_files_dir and item != zip_path:
                    shutil.move(str(item), str(release_files_dir))

            shutil.make_archive(str(release_dir / zip_name), "zip", release_files_dir)

            print("Release package created successfully!")

    except Exception as e:
        clear_release_by_error()
        print(f"Error creating release: {str(e)}")
        raise


if __name__ == "__main__":
    args = parse_args()
    create_release(version=args.version)
