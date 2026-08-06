import os

import PyInstaller.__main__

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PyInstaller.__main__.run([
    "src/main.py",
    "--name=FileOrganizer",
    "--onefile",
    "--windowed",
    f"--add-data={os.path.join(project_root, 'src/locales')};locales",
    "--clean",
    "--noconsole",
])
