from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                              QListWidget, QPushButton, QComboBox, QMessageBox,
                              QInputDialog, QWidget, QSplitter, QFrame)
from PySide6.QtCore import Qt
from core.database import DatabaseManager
from gettext import gettext as _

class FileTypeManagerDialog(QDialog):
    """Dialog for managing file types."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(_("File Type Manager"))
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.load_folders()
        self.retranslate_ui()

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)

        # Folder management section
        folder_section = QFrame()
        folder_section.setFrameShape(QFrame.StyledPanel)
        folder_layout = QVBoxLayout(folder_section)
        folder_layout.setSpacing(10)

        folder_header = QLabel("<b>Folder Management</b>")
        folder_header.setObjectName("folder_header")
        folder_layout.addWidget(folder_header)

        # Folder selection with buttons
        folder_control_layout = QHBoxLayout()
        folder_control_layout.addWidget(QLabel("Folder:"))

        self.folder_combo = QComboBox()
        self.folder_combo.setEditable(True)
        folder_control_layout.addWidget(self.folder_combo, 1)

        self.add_folder_btn = QPushButton("New Folder")
        self.add_folder_btn.clicked.connect(self.add_folder)
        folder_control_layout.addWidget(self.add_folder_btn)

        self.rename_folder_btn = QPushButton("Rename")
        self.rename_folder_btn.clicked.connect(self.rename_folder)
        folder_control_layout.addWidget(self.rename_folder_btn)

        self.delete_folder_btn = QPushButton("Delete")
        self.delete_folder_btn.clicked.connect(self.delete_folder)
        folder_control_layout.addWidget(self.delete_folder_btn)

        folder_layout.addLayout(folder_control_layout)

        # Extensions section
        extension_section = QFrame()
        extension_section.setFrameShape(QFrame.StyledPanel)
        extension_layout = QVBoxLayout(extension_section)
        extension_layout.setSpacing(10)

        extension_header = QLabel("<b>Extensions Management</b>")
        extension_header.setObjectName("extension_header")
        extension_layout.addWidget(extension_header)

        # Extensions list
        self.extension_list = QListWidget()
        extension_layout.addWidget(self.extension_list)

        # Add extension controls
        add_ext_layout = QHBoxLayout()
        self.new_extension = QLineEdit()
        self.new_extension.setPlaceholderText("New extension (e.g. .pdf)")
        add_ext_layout.addWidget(self.new_extension, 1)

        self.add_ext_btn = QPushButton("Add")
        self.add_ext_btn.clicked.connect(self.add_extension)
        add_ext_layout.addWidget(self.add_ext_btn)

        self.remove_ext_btn = QPushButton("Remove Selected")
        self.remove_ext_btn.clicked.connect(self.remove_extension)
        add_ext_layout.addWidget(self.remove_ext_btn)

        extension_layout.addLayout(add_ext_layout)

        # Add sections to main layout
        layout.addWidget(folder_section)
        layout.addWidget(extension_section)

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

        # Enable/disable buttons based on selection
        self.update_button_states()

    def folder_changed(self):
        """Update extensions list when folder selection changes."""
        folder_name = self.folder_combo.currentText()
        self.extension_list.clear()

        if folder_name:
            file_types = self.db_manager.get_file_types()
            if folder_name in file_types:
                for ext in sorted(file_types[folder_name]):
                    self.extension_list.addItem(ext)

        # Update button states
        self.update_button_states()

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

        # Update button states
        self.update_button_states()

    def remove_extension(self):
        """Remove the selected extension from the current folder."""
        selected_items = self.extension_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select an extension to remove")
            return

        folder_name = self.folder_combo.currentText()
        extension = selected_items[0].text()

        # Check if this is the last extension in the folder
        if self.db_manager.get_folder_count(folder_name) <= 1:
            reply = QMessageBox.question(
                self,
                "Confirm Folder Deletion",
                f"This is the last extension for folder '{folder_name}'. Remove the folder completely?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                if self.db_manager.delete_folder(folder_name):
                    self.load_folders()
                    return
            else:
                return  # User canceled

        # Remove from database
        if self.db_manager.remove_file_type(folder_name, extension):
            # Remove from list
            row = self.extension_list.row(selected_items[0])
            self.extension_list.takeItem(row)

            # Update button states
            self.update_button_states()
        else:
            QMessageBox.warning(self, "Error", f"Failed to remove extension {extension}")

    def add_folder(self):
        """Add a new folder."""
        folder_name, ok = QInputDialog.getText(
            self,
            "New Folder",
            "Enter folder name:"
        )

        if ok and folder_name:
            # Folders are created implicitly by adding a file type
            # Show dialog to add first extension
            extension, ok = QInputDialog.getText(
                self,
                "Add Extension",
                f"Enter first extension for folder '{folder_name}':"
            )

            if ok and extension:
                # Ensure extension starts with a dot
                if not extension.startswith('.'):
                    extension = '.' + extension

                # Add to database
                if self.db_manager.add_file_type(folder_name, extension):
                    # Update UI
                    self.load_folders()

                    # Select the new folder
                    index = self.folder_combo.findText(folder_name)
                    if index >= 0:
                        self.folder_combo.setCurrentIndex(index)
                else:
                    QMessageBox.warning(self, "Error", f"Failed to create folder {folder_name}")

    def rename_folder(self):
        """Rename the current folder."""
        old_name = self.folder_combo.currentText()

        if not old_name:
            QMessageBox.warning(self, "Warning", "Please select a folder to rename")
            return

        new_name, ok = QInputDialog.getText(
            self,
            "Rename Folder",
            "Enter new folder name:",
            text=old_name
        )

        if ok and new_name and new_name != old_name:
            # Check if the new name already exists
            file_types = self.db_manager.get_file_types()
            if new_name in file_types:
                reply = QMessageBox.question(
                    self,
                    "Confirm Merge",
                    f"Folder '{new_name}' already exists. Merge extensions from '{old_name}'?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply != QMessageBox.Yes:
                    return  # User canceled

            # Rename in database
            if self.db_manager.rename_folder(old_name, new_name):
                # Update UI
                self.load_folders()

                # Select the renamed folder
                index = self.folder_combo.findText(new_name)
                if index >= 0:
                    self.folder_combo.setCurrentIndex(index)
            else:
                QMessageBox.warning(self, "Error", f"Failed to rename folder {old_name}")

    def delete_folder(self):
        """Delete the current folder and all its extensions."""
        folder_name = self.folder_combo.currentText()

        if not folder_name:
            QMessageBox.warning(self, "Warning", "Please select a folder to delete")
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Delete folder '{folder_name}' and all its extensions?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Delete from database
            if self.db_manager.delete_folder(folder_name):
                # Update UI
                self.load_folders()
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete folder {folder_name}")

    def update_button_states(self):
        """Enable/disable buttons based on current selection."""
        has_folder = bool(self.folder_combo.currentText())
        has_extension = self.extension_list.count() > 0
        has_selected_ext = bool(self.extension_list.selectedItems())

        # Update folder button states
        self.rename_folder_btn.setEnabled(has_folder)
        self.delete_folder_btn.setEnabled(has_folder)

        # Update extension button states
        self.add_ext_btn.setEnabled(has_folder)
        self.remove_ext_btn.setEnabled(has_selected_ext)

    def retranslate_ui(self):
        """Update all UI texts with the current language."""
        self.setWindowTitle(_("File Type Manager"))

        # Folder management section
        folder_header = self.findChild(QLabel, "folder_header")
        if folder_header:
            folder_header.setText(_("<b>Folder Management</b>"))

        self.add_folder_btn.setText(_("New Folder"))
        self.rename_folder_btn.setText(_("Rename"))
        self.delete_folder_btn.setText(_("Delete"))

        # Extensions management section
        extension_header = self.findChild(QLabel, "extension_header")
        if extension_header:
            extension_header.setText(_("<b>Extensions Management</b>"))

        self.add_ext_btn.setText(_("Add"))
        self.remove_ext_btn.setText(_("Remove Selected"))
        self.close_btn.setText(_("Close"))

        # Labels
        folder_label = self.findChild(QLabel, "folder_label")
        if folder_label:
            folder_label.setText(_("Folder:"))
