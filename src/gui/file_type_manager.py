from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                              QListWidget, QPushButton, QComboBox, QMessageBox)
from PySide6.QtCore import Qt
from core.database import DatabaseManager

class FileTypeManagerDialog(QDialog):
    """Dialog for managing file types."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Type Manager")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.load_folders()

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)

        # Folder selection
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Folder:"))
        self.folder_combo = QComboBox()
        self.folder_combo.setEditable(True)
        folder_layout.addWidget(self.folder_combo)
        layout.addLayout(folder_layout)

        # Extensions list
        extensions_layout = QVBoxLayout()
        extensions_layout.addWidget(QLabel("Extensions:"))
        self.extension_list = QListWidget()
        extensions_layout.addWidget(self.extension_list)

        # Add extension controls
        add_ext_layout = QHBoxLayout()
        self.new_extension = QLineEdit()
        self.new_extension.setPlaceholderText("New extension (e.g. .pdf)")
        add_ext_layout.addWidget(self.new_extension)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_extension)
        add_ext_layout.addWidget(self.add_btn)
        extensions_layout.addLayout(add_ext_layout)

        # Remove extension button
        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self.remove_extension)
        extensions_layout.addWidget(self.remove_btn)

        layout.addLayout(extensions_layout)

        # Bottom buttons
        buttons_layout = QHBoxLayout()
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.close_btn)
        layout.addLayout(buttons_layout)

        # Connect signals
        self.folder_combo.currentTextChanged.connect(self.folder_changed)

    def load_folders(self):
        """Load folder names from database."""
        file_types = self.db_manager.get_file_types()
        self.folder_combo.clear()

        # Add folders to combo box
        for folder_name in sorted(file_types.keys()):
            self.folder_combo.addItem(folder_name)

    def folder_changed(self):
        """Update extensions list when folder selection changes."""
        folder_name = self.folder_combo.currentText()
        self.extension_list.clear()

        if folder_name:
            file_types = self.db_manager.get_file_types()
            if folder_name in file_types:
                for ext in sorted(file_types[folder_name]):
                    self.extension_list.addItem(ext)

    def add_extension(self):
        """Add a new extension to the current folder."""
        folder_name = self.folder_combo.currentText()
        extension = self.new_extension.text().strip()

        if not folder_name:
            QMessageBox.warning(self, "Warning", "Please select or enter a folder name")
            return

        if not extension:
            QMessageBox.warning(self, "Warning", "Please enter an extension")
            return

        # Ensure extension starts with a dot
        if not extension.startswith('.'):
            extension = '.' + extension

        # Add to database
        if self.db_manager.add_file_type(folder_name, extension):
            self.extension_list.addItem(extension)
            self.new_extension.clear()

            # Refresh folders list if this was a new folder
            self.load_folders()

            # Select the current folder again
            index = self.folder_combo.findText(folder_name)
            if index >= 0:
                self.folder_combo.setCurrentIndex(index)
        else:
            QMessageBox.warning(self, "Error", f"Failed to add extension {extension}")

    def remove_extension(self):
        """Remove the selected extension from the current folder."""
        selected_items = self.extension_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select an extension to remove")
            return

        folder_name = self.folder_combo.currentText()
        extension = selected_items[0].text()

        # Remove from database
        if self.db_manager.remove_file_type(folder_name, extension):
            # Remove from list
            row = self.extension_list.row(selected_items[0])
            self.extension_list.takeItem(row)
        else:
            QMessageBox.warning(self, "Error", f"Failed to remove extension {extension}")
