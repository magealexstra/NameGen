# Kubuntu Image Batch Renamer

A Qt-based application for batch renaming image files with preview capabilities, designed for Kubuntu and other Linux distributions.

## Features
- File browser with folder navigation
- Thumbnail image previews with multi-selection
- Loads all images in a folder without artificial limits
- Multiple renaming schemes:
  - Custom name patterns
  - Find and replace text
  - Case conversion (lowercase, UPPERCASE, Title Case)
  - Sequential numbering with customizable options
- Real-time preview of renamed files
- Conflict detection and validation to prevent overwrites and invalid filenames
- Option to move files to a different folder
- Skip confirmation option for faster batch processing

## Requirements
- Python 3.8+
- PySide6 6.6.0 or newer
- Pillow 10.0.0 or newer

## Installation
```bash
# Clone the repository
git clone https://github.com/magealexstra/NameGen
cd NameGen

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# Or on Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application
```bash
# Make sure your virtual environment is activated
python3 src/main.py
```

## How to Use

1. **Navigation**: Browse folders using the file tree on the left
2. **Selection**: Select one or more images in the center pane
3. **Configure**: Set up renaming options in the right panel:
   - **Name Template**: Enter a new name pattern
   - **Find/Replace**: Specify text to find and replace
   - **Case**: Change text case (preserve, lowercase, UPPERCASE, Title Case)
   - **Sequential Numbers**: Add sequential numbers with custom settings
   - **Destination**: Optionally move files to a different folder
4. **Preview**: View how files will be renamed in the preview section
5. **Apply**: Click "Rename Files" to apply the changes
6. **Skip Confirmation**: Check the "Skip confirmation" option to avoid confirmation dialogs

## Development

### Running Tests (optional)
Tests are excluded from version control but can be run locally if present:
```bash
python3 -m unittest discover tests
python3 tests/test_renamer_functionality.py
```

### Project Structure
- `src/main.py` - Application entry point
- `src/renamer_engine.py` - Core renaming functionality
- `src/ui_module.py` - Qt-based user interface
- `tests/` - Unit tests (ignored in git)
- `Data/` - Sample images for testing (ignored in git)

## License
MIT
