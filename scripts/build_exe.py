import PyInstaller.__main__
import os
from release_version import VersionManager

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
version_manager = VersionManager("version.txt")
version = version_manager.load_version()

PyInstaller.__main__.run([
    'src/main.py',  # Your main script
    '--name=FileOrganizer',  # Name of the executable
    '--onefile',  # Create a single executable file
    # "--onedir",  # Create a directory with the executable and dependencies
    '--windowed',  # Don't show console window
    f'--add-data={os.path.join(project_root, "src/locales")};locales',  # Include translations
    # '--icon=resources/icon.ico',  # Optional: Add an icon
    '--clean',  # Clean cache before building
    '--noconsole',  # No console window
])