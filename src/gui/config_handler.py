import os
from dotenv import load_dotenv, set_key

class ConfigHandler:
    """Handles loading and saving configuration."""
    @staticmethod
    def load_config():
        """Load configuration from .env file."""
        load_dotenv()
        return {
            'SOURCE_FOLDER': os.getenv('SOURCE_FOLDER', ''),
            'ORGANIZED_FOLDER': os.getenv('ORGANIZED_FOLDER', ''),
            'UNORGANIZED_FOLDER': os.getenv('UNORGANIZED_FOLDER', ''),
            'DEBUG': os.getenv('DEBUG', 'False'),
            'USE_CREATION_DATE': os.getenv('USE_CREATION_DATE', 'False'),
            'FORCE_DATE': os.getenv('FORCE_DATE', 'False'),
            'DATE_FOLDERS': os.getenv('DATE_FOLDERS', 'False')
        }

    @staticmethod
    def save_config(config: dict):
        """Save configuration to .env file."""
        env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        for key, value in config.items():
            set_key(env_path, key, value)