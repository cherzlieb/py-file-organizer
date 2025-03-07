import os
import logging
from core.database import DatabaseManager
from utils.file_types import FILE_TYPES  # Import the default file types

class ConfigHandler:
    """Handles loading and saving configuration using SQLite database."""

    @staticmethod
    def load_config():
        """Load configuration from database."""
        try:
            db_manager = DatabaseManager()

            # Initialize database if needed
            db_manager.initialize_database()

            # Define default config
            default_config = {
                'SOURCE_FOLDER': '',
                'ORGANIZED_FOLDER': '',
                'UNORGANIZED_FOLDER': '',
                'DEBUG': 'False',
                'USE_CREATION_DATE': 'False',
                'FORCE_DATE': 'False',
                'DATE_FOLDERS': 'False',
                'LANGUAGE': 'en'
            }

            # Populate with default values if empty
            db_manager.populate_default_config(default_config)

            # Populate with default file types if empty
            db_manager.populate_default_file_types(FILE_TYPES)

            # Get current config
            return db_manager.get_config()

        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            # Return default config if loading fails
            return default_config

    @staticmethod
    def save_config(config: dict):
        """Save configuration to database."""
        try:
            db_manager = DatabaseManager()
            db_manager.update_config(config)
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")

    @staticmethod
    def get_file_types():
        """Get file types from database."""
        try:
            db_manager = DatabaseManager()
            return db_manager.get_file_types()
        except Exception as e:
            logging.error(f"Error getting file types: {e}")
            return {}
