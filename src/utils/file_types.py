from core.database import DatabaseManager

# Define default file types
FILE_TYPES = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.raw', '.ico', '.psd', '.ai', '.eps'],
    'music': ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.wma', '.ogg', '.mid', '.midi'],
    'documents': ['.pdf', '.docx', '.txt', '.pptx', '.html', '.tex', '.doc', '.rtf', '.odt', '.md', '.epub', '.mobi'],
    'videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'],
    'archives': ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz', '.iso', '.tgz'],
    '3d-prints': ['.3mf', '.stl', '.obj', '.gcode', '.amf'],
    'executables': ['.exe', '.msi', '.bat', '.cmd', '.ps1', '.sh'],
    'vs-extensions': ['.vsix'],
    'disk-images': ['.iso', '.img', '.vhd', '.vmdk'],
    'poe': ['.filter'],
    'spreadsheets': ['.csv', '.xlsx', '.xls', '.ods'],
    'ai-models': ['.safetensors', '.onnx', '.pth', '.h5', '.pkl'],
    'psx-projects': ['.psxprj'],
    'windows-apps': ['.appx', '.appxbundle', '.appinstaller', '.msix'],
    'config': ['.yml', '.yaml', '.json', '.xml', '.ini', '.conf', '.toml'],
    'databases': ['.sqlite3', '.db', '.sqlite', '.sql', '.mdb', '.accdb'],
    'audiobooks': ['.aax', '.m4b'],
    'code': ['.py', '.js', '.java', '.cpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift'],
    'fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
    'ebooks': ['.epub', '.mobi', '.azw', '.azw3', '.pdf'],
    'design': ['.psd', '.ai', '.xd', '.sketch', '.fig'],
    'subtitles': ['.srt', '.sub', '.ass', '.vtt'],
    'torrents': ['.torrent'],
    'backups': ['.bak', '.backup'],
    'certificates': ['.crt', '.cer', '.key', '.pem'],
    'export-lib': ['.exp'],
    'codesys-lib': ['.library'],
    'bin-files': ['.bin'],
}

def get_file_types():
    """Get file types from database or default if database access fails."""
    try:
        db_manager = DatabaseManager()
        db_manager.initialize_database()

        # Populate default file types if database is empty
        db_manager.populate_default_file_types(FILE_TYPES)

        # Return file types from database
        return db_manager.get_file_types()
    except Exception as e:
        # Fallback to default file types
        return FILE_TYPES
