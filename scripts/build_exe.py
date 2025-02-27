import PyInstaller.__main__
import os

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PyInstaller.__main__.run([
    'src/main.py',  # Your main script
    '--name=FileOrganizer',  # Name of the executable
    '--onefile',  # Create a single executable file
    '--windowed',  # Don't show console window
    f'--add-data={os.path.join(project_root, "src/locales")};locales',  # Include translations
    # '--icon=resources/icon.ico',  # Optional: Add an icon
    '--clean',  # Clean cache before building
    '--noconsole',  # No console window
])