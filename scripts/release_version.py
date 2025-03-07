import os

# Klasse für die Verwaltung der Versionsnummer
class VersionManager:
    def __init__(self, file_path="version.txt"):
        self.file_path = file_path

    def load_version(self):
        """Lädt die aktuelle Version aus der Datei oder setzt eine Standardversion."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return file.read().strip()
        return "0.0.0"  # Standardversion

    def save_version(self, version):
        """Speichert die Version in die Datei."""
        with open(self.file_path, 'w') as file:
            file.write(version)

    def increment_version(self, version, part):
        """Hochzählen der Version."""
        major, minor, patch = map(int, version.split('.'))
        
        part_lower = part.lower()
        if part_lower not in ["major", "minor", "patch"]:
            raise ValueError("Ungültige Eingabe. Bitte wähle MAJOR, MINOR oder PATCH.")
        
        if part_lower == "major":
            major += 1
            minor = 0
            patch = 0
        elif part_lower == "minor":
            minor += 1
            patch = 0
        elif part_lower == "patch":
            patch += 1
            
        return f"{major}.{minor}.{patch}"

    def set_version(self, part=None):
        """Setzt oder erhöht die Version basierend auf der Eingabe."""
        current_version = self.load_version()
        if part:
            return self.increment_version(current_version, part)
        return current_version  # Behält die alte Version bei
