import os
import shutil
import subprocess
import sys
from pathlib import Path


def create_release():
    """Create a release package."""
    try:
        # Compile translations
        compile_script = Path(__file__).parent / "compile_translations.py"
        print(f"Compiling translations using: {compile_script}")
        subprocess.run([sys.executable, str(compile_script)], check=True)

        # Setup paths
        root_dir = Path(__file__).parent.parent
        release_dir = root_dir / "Release"
        dist_dir = root_dir / "dist"
        version = "v0.1.0"
        zip_name = f"FileOrganizer-{version}"

        print(f"Creating release in: {release_dir}")

        # Clean old release files
        if release_dir.exists():
            shutil.rmtree(release_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)

        # Create release directory structure
        (release_dir / "config").mkdir(parents=True)
        (release_dir / "locales/de/LC_MESSAGES").mkdir(parents=True)
        (release_dir / "locales/en/LC_MESSAGES").mkdir(parents=True)

        # Build executable using absolute path
        build_script = root_dir / "scripts" / "build_exe.py"
        print(f"Building executable using: {build_script}")
        subprocess.run([sys.executable, str(build_script)], check=True)

        # Copy files to release directory
        if dist_dir.exists() and (dist_dir / "FileOrganizer.exe").exists():
            print("Copying files to release directory...")
            # Copy executable
            shutil.copy2(dist_dir / "FileOrganizer.exe", release_dir)

            # Copy and rename .env.example to .env
            shutil.copy2(root_dir / ".env.example",
                         release_dir / "config" / ".env")

            # Copy translation files
            for lang in ['de', 'en']:
                src_mo = root_dir / \
                    f"src/locales/{lang}/LC_MESSAGES/messages.mo"
                dst_mo = release_dir / \
                    f"locales/{lang}/LC_MESSAGES/messages.mo"
                if src_mo.exists():
                    shutil.copy2(src_mo, dst_mo)
                else:
                    print(f"Warning: Translation file not found: {src_mo}")

            # Create README.txt
            with open(release_dir / "README.txt", "w", encoding="utf-8") as f:
                f.write("""File Organizer v1.0.0

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

            # Create ZIP file in Release directory
            zip_path = release_dir / f"{zip_name}.zip"
            print(f"Creating ZIP file: {zip_path}")

            # Create archive of all files in release_dir
            release_files_dir = release_dir / "files"

            # Move all release files to a subdirectory
            if release_files_dir.exists():
                shutil.rmtree(release_files_dir)
            release_files_dir.mkdir()

            # Move all files except the zip to the files directory
            for item in release_dir.iterdir():
                if item != release_files_dir and item != zip_path:
                    shutil.move(str(item), str(release_files_dir))

            # Create ZIP from files directory
            shutil.make_archive(str(release_dir / zip_name),
                                'zip', release_files_dir)

            print("Release package created successfully!")

        else:
            print("Error: FileOrganizer.exe was not created successfully!")

    except Exception as e:
        print(f"Error creating release: {str(e)}")
        raise


if __name__ == "__main__":
    create_release()
