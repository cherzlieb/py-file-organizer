# File Organizer

This project is a simple Python application that automatically sorts files in your Downloads folder by organizing them into separate folders based on their file types. This helps keep your Downloads folder tidy and makes it easier to find files.

## Features

-   Automatically sorts files into appropriate folders based on their types
-   Supports various file types
-   Automatically adds modification or creation date to the filename (configurable)
-   Moves folders to an "Unorganized" folder
-   Cleans up filenames
-   Configuration via .env file
-   Detailed logging

## Project Structure

```path
file-organizer/
├── src/
│   ├── main.py                 # Hauptprogramm
│   ├── config.py               # Konfigurationsklassen
│   └── utils/
│       ├── file_utils.py       # Hauptlogik für Dateiorganisation
│       ├── file_types.py       # Definition der Dateitypen
│       ├── file_operations.py  # Dateioperationen
│       ├── date_utils.py       # Datumsfunktionen
│       ├── path_utils.py       # Pfadoperationen
│       └── filename_utils.py   # Dateinamenverarbeitung
├── logs/                       # Logdateien (wird automatisch erstellt)
├── .env.example                # Beispiel-Umgebungsvariablen
├── requirements.txt            # Python-Abhängigkeiten
└── README.md                   # Projektdokumentation
```

## Prerequisites

To run this project, you need Python installed on your computer. Additional dependencies are listed in the `requirements.txt` file.

## Installation

1. Clone the repository to your local computer:

    ```bash
    git clone https://github.com/cherzlieb/py-file-organizer
    ```

2. Navigate to the project directory:

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

1. Copy the `.env.example` file to `.env`:

    ```bash
    cp .env.example .env
    ```

2. Adjust the paths in the `.env` file:

    ```ini
    SOURCE_FOLDER = ""      # Specify the path to be sorted.
    ORGANIZED_FOLDER = ""   # Specify the path where sorted files should go (in the Organized subfolder).
    UNORGANIZED_FOLDER = "" # Specify the path where unsorted folders should go (in the Unorganized subfolder).
    LOG_FILE = ""           # Path to the log file, including the name (located in the project folder).
    DEBUG = False           # Specify whether to enable debug mode.
    ```

## Usage

Run the program:

```bash
python src/main.py
```

The program will:

-   Sort files by type and move them to corresponding subfolders
-   Prepend the creation date to the filename
-   Move folders to an "Unorganized" folder
-   Display progress in the console

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. For more details, see the LICENSE file.

## Changes

The main changes are:

-   Updated project structure
-   New configuration method via `.env`
-   More precise description of date functionality
-   Addition of the new logging feature
-   Removal of the outdated `DOWNLOADS_FOLDER` reference
-   More accurate description of the module structure
