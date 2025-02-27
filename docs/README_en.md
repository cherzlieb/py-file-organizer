# File Organizer

This project is a simple Python application that automatically organizes files in your downloads folder by sorting them into separate folders based on their file types. This helps keep your downloads folder tidy and makes it easier to find files.

## Features

- Automatic sorting of files into appropriate folders based on their types
- Support for various file types
- Automatically adds modification or creation date to filenames (configurable)
- Moves folders to an "Unorganized" folder
- Filename cleanup
- Configuration via .env file
- Detailed logging
- Graphical User Interface (GUI)
- Multi-language support (English/German)

## Project Structure

```path
file-organizer/
├── src/
│   ├── core/
│   │   ├── config.py           # Configuration classes
│   │   ├── constants.py        # Constants
│   │   └── translation.py      # Translation functions
│   ├── gui/
│   │   ├── components.py       # GUI components
│   │   ├── config_handler.py   # Configuration handling
│   │   └── main_window.py      # Main window
│   ├── utils/                  # Helper functions
│   │   ├── file_types.py       # File type definitions
│   │   └── file_utils.py       # File operations
│   └── main.py                 # Main program
├── locales/                    # Language files
│   ├── de/                     # German translations
│   └── en/                     # English translations
├── logs/                       # Log files
└── README.md                   # Documentation
```

## Prerequisites

To run this project, you need Python installed on your computer. Additional dependencies are listed in `requirements.txt`.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/cherzlieb/py-file-organizer
    ```

2. Change to the project directory:

    ```bash
    cd file-organizer
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    # Windows
    .\venv\Scripts\activate

    # Linux/Mac
    source venv/bin/activate
    ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Configuration can be done through the graphical user interface or the `.env` file.

### Via GUI (recommended)

Start the program and configure the settings in the main window:

1. Select your preferred language (English/German)
2. Specify the folder paths:
   - Source folder: The folder to be organized
   - Target folder: Folder for sorted files
   - Non-sortable: Folder for non-sortable items
3. Optionally enable:
   - Debug mode for detailed logging
   - Use creation date
   - Force date
   - Add date to folders
4. Click "Save Configuration"

Settings are automatically saved in the `.env` file.

### Manual Configuration (alternative)

Alternatively, you can edit the `.env` file directly:

```ini
SOURCE_FOLDER=""         # Source folder
ORGANIZED_FOLDER=""      # Target folder for sorted files
UNORGANIZED_FOLDER=""    # Folder for non-sortable items
LOG_FILE=""             # Path to log file
DEBUG=False             # Debug mode (True/False)
USE_CREATION_DATE=False # Use creation date (True/False)
FORCE_DATE=False        # Force date (True/False)
DATE_FOLDERS=False      # Add date to folders (True/False)
LANGUAGE="en"           # Language (en/de)
```

## Usage

Run the program:

```bash
python src/main.py
```

### Graphical User Interface (GUI)

After starting the program, the main window appears with the following options:

- **Language**: Choose between English and German
- **Source Folder**: The folder to be organized
- **Target Folder**: Folder for sorted files
- **Non-sortable**: Folder for non-sortable items
- **Debug Mode**: Enables detailed logging
- **Use Creation Date**: Uses creation date instead of modification date
- **Force Date**: Always adds a date
- **Add Date to Folders**: Also adds dates to folders

Settings are automatically saved and restored on next startup.

The program will:

- Sort files by type and move them to appropriate subfolders
- Prepend the creation date to the filename
- Move folders to an "Unorganized" folder
- Show progress in the console

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Changes

Key changes include:

- Updated project structure
- New configuration method via `.env`
- More precise description of date functionality
- Addition of new logging feature
- Removal of outdated `DOWNLOADS_FOLDER` reference
- More detailed module structure description
