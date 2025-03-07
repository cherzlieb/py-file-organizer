import sys
import os
import logging
from dotenv import load_dotenv
from utils.file_utils import organize_files_by_type
from utils.file_types import FILE_TYPES
from core.config import OrganizerConfig, Config
from PySide6.QtWidgets import QApplication
from gui.main_window import FileOrganizerWindow

# Load environment variables
load_dotenv()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Setup logging
log_file = resource_path('logs/file_organizer.log')
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

# Get paths from environment variables
SOURCE_FOLDER = os.getenv('SOURCE_FOLDER')
ORGANIZED_FOLDER = os.getenv('ORGANIZED_FOLDER')
UNORGANIZED_FOLDER = os.getenv('UNORGANIZED_FOLDER')
USE_CREATION_DATE = os.getenv('USE_CREATION_DATE')
FORCE_DATE = os.getenv('FORCE_DATE')

# Add debug output to verify paths
if os.getenv('DEBUG') == 'True':
    logger.debug(f"Source folder path: {SOURCE_FOLDER}")
    logger.debug(f"Organized folder path: {ORGANIZED_FOLDER}")
    logger.debug(f"Unorganized folder path: {UNORGANIZED_FOLDER}")

# Check if source folder exists
if not SOURCE_FOLDER or not os.path.exists(SOURCE_FOLDER):
    logger.warning(f"Source folder not found or not set: {SOURCE_FOLDER}")


def create_config() -> OrganizerConfig:
    """Creates and returns the configuration object."""
    return OrganizerConfig(
        source_folder=SOURCE_FOLDER,
        organized_folder=ORGANIZED_FOLDER,
        unorganized_folder=UNORGANIZED_FOLDER,
        file_types=FILE_TYPES,
        logger=logger,
        use_creation_date=USE_CREATION_DATE,
        force_date=FORCE_DATE
    )


def main() -> None:
    """Main entry point of the application."""
    # Create and show GUI
    app = QApplication(sys.argv)
    window = FileOrganizerWindow(logger)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
