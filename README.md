# File: /file-organizer/file-organizer/README.md

# File Organizer

This project is a simple Python application that organizes files in your Downloads folder by sorting them into separate folders based on their file types. It helps keep your Downloads folder tidy and makes it easier to find files.

## Features

- Automatically sorts files into designated folders based on their types (e.g., images, music, documents).
- Supports various file types including images, audio files, documents, and more.

## Project Structure

```
file-organizer
├── src
│   ├── main.py          # Entry point of the application
│   └── utils
│       └── file_utils.py # Utility functions for file handling
├── requirements.txt     # List of dependencies
└── README.md            # Project documentation
```

## Requirements

To run this project, you need to have Python installed on your machine. Additionally, you may need to install the required dependencies listed in the `requirements.txt` file.

## Installation

1. Clone the repository to your local machine:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd file-organizer
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To organize your Downloads folder, run the following command:
```
python src/main.py
```

Make sure to adjust the script if your Downloads folder is located in a different path.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.