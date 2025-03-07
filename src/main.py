import sys
import os
import logging
from utils.file_utils import organize_files_by_type
from core.config import OrganizerConfig, Config
from core.database import DatabaseManager
from utils.file_types import get_file_types
from gui.main_window import FileOrganizerWindow
from PySide6.QtWidgets import QApplication

# Setup logging
log_file = 'logs/file_organizer.log'
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def initialize_database():
    """Initialize the database with default values."""
    try:
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

def create_config() -> OrganizerConfig:
    """Creates and returns the configuration object from database."""
    from gui.config_handler import ConfigHandler

    # Get configuration from database
    config_dict = ConfigHandler.load_config()

    # Get file types from database
    file_types = get_file_types()

    # Parse boolean values
    use_creation_date = config_dict.get('USE_CREATION_DATE', 'False').lower() == 'true'
    force_date = config_dict.get('FORCE_DATE', 'False').lower() == 'true'
    date_folders = config_dict.get('DATE_FOLDERS', 'False').lower() == 'true'

    return OrganizerConfig(
        source_folder=config_dict.get('SOURCE_FOLDER', ''),
        organized_folder=config_dict.get('ORGANIZED_FOLDER', ''),
        unorganized_folder=config_dict.get('UNORGANIZED_FOLDER', ''),
        file_types=file_types,
        logger=logger,
        use_creation_date=use_creation_date,
        force_date=force_date,
        date_folders=date_folders
    )

def main() -> None:
    """Main entry point of the application."""
    # Initialize database
    initialize_database()

    # Create and show GUI
    app = QApplication(sys.argv)
    window = FileOrganizerWindow(logger)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
