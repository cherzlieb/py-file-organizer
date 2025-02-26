import sys
import os
import logging
from dotenv import load_dotenv
from utils.file_utils import organize_files_by_type
from utils.file_types import FILE_TYPES
from config import OrganizerConfig, Config

# Load environment variables
load_dotenv()

# Setup logging with file output
log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'file_organizer.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=Config.LOG_LEVEL,
    format=Config.LOG_FORMAT,
    datefmt=Config.DATE_FMT,  # Fügt das neue Datumsformat hinzu
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)  # Behält auch die Konsolenausgabe
    ]
)
logger = logging.getLogger(__name__)

# Get paths from environment variables
SOURCE_FOLDER = os.getenv('SOURCE_FOLDER')
ORGANIZED_FOLDER = os.getenv('ORGANIZED_FOLDER')
UNORGANIZED_FOLDER = os.getenv('UNORGANIZED_FOLDER')

# Add debug output to verify paths
if os.getenv('DEBUG') == 'True':
    logger.debug(f"Source folder path: {SOURCE_FOLDER}")
    logger.debug(f"Organized folder path: {ORGANIZED_FOLDER}")
    logger.debug(f"Unorganized folder path: {UNORGANIZED_FOLDER}")

# Check if source folder exists
if not os.path.exists(SOURCE_FOLDER):
    logger.warning(f"Source folder not found at {SOURCE_FOLDER}")


def create_config() -> OrganizerConfig:
    """Creates and returns the configuration object."""
    return OrganizerConfig(
        source_folder=SOURCE_FOLDER,
        organized_folder=ORGANIZED_FOLDER,
        unorganized_folder=UNORGANIZED_FOLDER,
        file_types=FILE_TYPES,
        logger=logger,
        use_creation_date=False,
        force_date=False
    )

def main() -> None:
    """Main entry point of the application."""
    load_dotenv()
    
    config = create_config()
    
    try:
        organize_files_by_type(config)
    except Exception as e:
        logger.error(f"Error during file organization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
