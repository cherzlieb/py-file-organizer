import os
import shutil
import glob

def delete_files_with_pattern(pattern):
    files = glob.glob(pattern)  # Sucht alle Dateien, die dem Muster entsprechen
    for file in files:
        try:
            os.remove(file)
            print(f"Datei '{file}' wurde gelöscht.")
        except Exception as e:
            print(f"Fehler beim Löschen von '{file}': {e}")

# Funktion, um Ordner zu löschen
def delete_folder(folder_name):
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        try:
            shutil.rmtree(folder_name)
            print(f"Ordner '{folder_name}' wurde gelöscht.")
        except Exception as e:
            print(f"Fehler beim Löschen von '{folder_name}': {e}")

# Hauptfunktion
def main():
    print("Lösche Verzeichnisse...")

    # Zu löschende Ordner
    folders_to_delete = ["build", "dist", "release"]
    for folder in folders_to_delete:
        delete_folder(folder)
        
    delete_files_with_pattern("FileOrganizer*.spec")