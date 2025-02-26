import os
import logging
from dotenv import load_dotenv
from utils.file_utils import organize_files
from utils.file_types import FILE_TYPES

# Load environment variables
load_dotenv()

# Setup logging with more detailed output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s'  # Simplified format for cleaner output
)
logger = logging.getLogger(__name__)

# Get paths from environment variables
DOWNLOADS_FOLDER = os.getenv('DOWNLOADS_FOLDER')
ORGANIZED_FOLDER = os.path.join(DOWNLOADS_FOLDER, os.getenv('ORGANIZED_FOLDER'))
UNORGANIZED_FOLDER = os.path.join(DOWNLOADS_FOLDER, os.getenv('UNORGANIZED_FOLDER'))

# Add debug output to verify paths
if DEBUG:
    print(f"Downloads folder path: {DOWNLOADS_FOLDER}")
    print(f"Organized folder path: {ORGANIZED_FOLDER}")
    print(f"Unorganized folder path: {UNORGANIZED_FOLDER}")

# Check if Downloads folder exists and list contents
if os.path.exists(DOWNLOADS_FOLDER):
    print("\nFiles in Downloads folder:")
    for file in os.listdir(DOWNLOADS_FOLDER):
        print(f"- {file}")
else:
    print(f"Warning: Downloads folder not found at {DOWNLOADS_FOLDER}")


if __name__ == "__main__":
    organize_files(
        download_folder=DOWNLOADS_FOLDER,
        organized_folder=ORGANIZED_FOLDER,
        unorganized_folder=UNORGANIZED_FOLDER,
        file_types=FILE_TYPES,
        logger=logger
    )
