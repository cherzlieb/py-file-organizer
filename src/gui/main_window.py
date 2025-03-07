from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QCheckBox, QPushButton, QMessageBox, QLabel, QComboBox)
from PySide6.QtCore import Qt, Signal
import os
import sys
import logging
from utils.file_utils import organize_files_by_type
from utils.file_types import FILE_TYPES
from utils.logger import update_debug_mode, get_logger
from core.config import OrganizerConfig
from core.translation import Translation
from .components import FolderEntryWidget
from .config_handler import ConfigHandler
from .file_type_manager import FileTypeManagerDialog
from gettext import gettext as _


class FileOrganizerWindow(QMainWindow):
    """Main window of the File Organizer application."""

    # Signal für Sprachänderung hinzufügen
    language_changed = Signal()

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.default_height = None

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Load initial configuration and set language BEFORE creating UI components
        config = ConfigHandler.load_config()
        initial_language = config.get('LANGUAGE', 'en')

        # Setup initial translation
        translator = Translation.setup_language(initial_language)
        translator.install()

        # Force update of gettext function
        import builtins
        builtins.__dict__['_'] = translator.gettext

        # Update global _ in current module
        global _
        _ = translator.gettext

        # Create and setup UI components with translations
        self.setup_language_selection()
        self.setup_folder_entries()
        self.setup_checkboxes()
        self.setup_buttons()

        # Add spacing at the bottom
        self.main_layout.addStretch()

        # Load configuration values
        self.load_config()

        # Update UI with initial translations
        self.retranslate_ui()

        # Store initial window size
        self.adjustSize()
        self.default_height = self.height()

        # Debug-Checkbox-Verbindung aktualisieren
        self.debug_cb.stateChanged.connect(self.toggle_debug)

    def setup_folder_entries(self):
        """Setup folder entry widgets."""
        self.folder_entries = {}
        folders = [
            ('SOURCE_FOLDER', 'Source Folder:'),
            ('ORGANIZED_FOLDER', 'Organized Folder:'),
            ('UNORGANIZED_FOLDER', 'Unorganized Folder:')
        ]

        for key, label in folders:
            entry = FolderEntryWidget(label)
            self.folder_entries[key] = entry
            self.main_layout.addWidget(entry)

    def setup_checkboxes(self):
        """Setup checkbox widgets."""
        checkbox_container = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_container)

        self.debug_cb = QCheckBox("Debug Mode")
        self.creation_date_cb = QCheckBox("Use Creation Date")
        self.force_date_cb = QCheckBox("Force Date")
        self.date_folders_cb = QCheckBox("Add Date to Folders")

        for cb in [self.debug_cb, self.creation_date_cb,
                   self.force_date_cb, self.date_folders_cb]:
            checkbox_layout.addWidget(cb)

        self.main_layout.addWidget(checkbox_container)

    def setup_language_selection(self):
        """Setup language selection dropdown."""
        language_container = QWidget()
        language_layout = QHBoxLayout(language_container)

        # Create label and store reference
        self.language_label = QLabel(_("Language:"))  # Store reference
        self.language_combo = QComboBox()

        # Add available languages
        for code, name in Translation.get_language_names().items():
            self.language_combo.addItem(name, code)

        # Set current language from config
        current_language = ConfigHandler.load_config().get('LANGUAGE', 'en')
        index = self.language_combo.findData(current_language)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

        # Connect signal for language change
        self.language_combo.currentIndexChanged.connect(self.change_language)

        language_layout.addWidget(self.language_label)  # Use stored reference
        language_layout.addWidget(self.language_combo)

        self.main_layout.addWidget(language_container)

    def setup_buttons(self):
        """Setup action buttons."""
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)

        start_button = QPushButton("Start Sorting")
        file_types_button = QPushButton("Manage File Types")  # Add this button

        start_button.clicked.connect(self.start_sorting)
        file_types_button.clicked.connect(self.open_file_type_manager)  # Add this connection

        button_layout.addWidget(start_button)
        button_layout.addWidget(file_types_button)  # Add this button

        self.main_layout.addWidget(button_container)

    def load_config(self):
        """Load configuration from .env file."""
        config = ConfigHandler.load_config()

        # Set folder entries
        for key, entry in self.folder_entries.items():
            entry.entry.setText(config[key])

        # Set checkboxes
        self.debug_cb.setChecked(config['DEBUG'].lower() == 'true')
        self.creation_date_cb.setChecked(
            config['USE_CREATION_DATE'].lower() == 'true')
        self.force_date_cb.setChecked(config['FORCE_DATE'].lower() == 'true')
        self.date_folders_cb.setChecked(
            config['DATE_FOLDERS'].lower() == 'true')

    def save_config(self):
        """Save configuration to .env file."""
        config = {
            'SOURCE_FOLDER': self.folder_entries['SOURCE_FOLDER'].entry.text(),
            'ORGANIZED_FOLDER': self.folder_entries['ORGANIZED_FOLDER'].entry.text(),
            'UNORGANIZED_FOLDER': self.folder_entries['UNORGANIZED_FOLDER'].entry.text(),
            'DEBUG': str(self.debug_cb.isChecked()),
            'USE_CREATION_DATE': str(self.creation_date_cb.isChecked()),
            'FORCE_DATE': str(self.force_date_cb.isChecked()),
            'DATE_FOLDERS': str(self.date_folders_cb.isChecked()),
            'LOG_FILE': "logs/file_organizer.log",
            'LANGUAGE': self.language_combo.currentData()
        }

        ConfigHandler.save_config(config)

    def toggle_debug(self):
        """Debug-Modus ändern und Logging aktualisieren."""
        debug_mode = self.debug_cb.isChecked()
        update_debug_mode(debug_mode)

        # Config speichern
        self.save_config()

    def start_sorting(self):
        """Start the file organization process."""
        try:
            # Debug-Modus aktualisieren
            debug_mode = self.debug_cb.isChecked()
            update_debug_mode(debug_mode)

            # Informationslog schreiben
            self.logger.debug("Starting file organization process")

            config = OrganizerConfig(
                source_folder=self.folder_entries['SOURCE_FOLDER'].entry.text(),
                organized_folder=self.folder_entries['ORGANIZED_FOLDER'].entry.text(),
                unorganized_folder=self.folder_entries['UNORGANIZED_FOLDER'].entry.text(),
                file_types=FILE_TYPES,
                logger=self.logger,
                use_creation_date=self.creation_date_cb.isChecked(),
                force_date=self.force_date_cb.isChecked(),
                date_folders=self.date_folders_cb.isChecked()
            )

            # Check if source folder exists
            if not os.path.exists(config.source_folder):
                error_msg = f"Source folder not found: {config.source_folder}"
                self.logger.error(error_msg)
                QMessageBox.warning(self, "Error", _(error_msg))
                return

            # Start organization process
            organize_files_by_type(config)

            success_msg = "File organization completed successfully!"
            self.logger.debug(success_msg)
            QMessageBox.information(self, "Success", _(success_msg))

        except Exception as e:
            error_msg = f"Error during file organization: {str(e)}"
            self.logger.error(error_msg)
            QMessageBox.critical(self, "Error", _(error_msg))

    def change_language(self):
        """Change application language."""
        language_code = self.language_combo.currentData()

        # Setup translation
        translator = Translation.setup_language(language_code)

        # Force update of gettext function
        import builtins
        builtins.__dict__['_'] = translator.gettext

        # Update global _ in current module
        global _
        _ = translator.gettext

        # Test translation immediately
        test_text = _("File Organizer")

        # Update UI
        self.retranslate_ui()

        # Signal auslösen für alle abhängigen Widgets
        self.language_changed.emit()

        # Save config
        config = ConfigHandler.load_config()
        config['LANGUAGE'] = language_code
        ConfigHandler.save_config(config)

    def retranslate_ui(self):
        """Update all UI texts with new language."""
        # Update window title
        self.setWindowTitle(_("File Organizer"))

        # Update language selector using stored reference
        self.language_label.setText(_("Language:"))

        # Update folder entries
        for key, entry in self.folder_entries.items():
            if key == 'SOURCE_FOLDER':
                entry.label.setText(_("Source Folder:"))
            elif key == 'ORGANIZED_FOLDER':
                entry.label.setText(_("Organized Folder:"))
            elif key == 'UNORGANIZED_FOLDER':
                entry.label.setText(_("Unorganized Folder:"))
            entry.browse_btn.setText(_("Browse"))

        # Update checkboxes
        self.debug_cb.setText(_("Debug Mode"))
        self.creation_date_cb.setText(_("Use Creation Date"))
        self.force_date_cb.setText(_("Force Date"))
        self.date_folders_cb.setText(_("Add Date to Folders"))

        # Update buttons
        for button in self.findChildren(QPushButton):
            if button.text() == "Save Configuration":
                button.setText(_("Save Configuration"))
            elif button.text() == "Start Sorting":
                button.setText(_("Start Sorting"))
            elif button.text() == "Manage File Types":
                button.setText(_("Manage File Types"))

    def open_file_type_manager(self):
        """Open the file type manager dialog."""
        dialog = FileTypeManagerDialog(self)
        dialog.exec()
