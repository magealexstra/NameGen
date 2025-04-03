# Checklist: Kubuntu Image Batch Renamer Project

## Phase 1: Project Setup & Core Dependencies

*   [ ] Initialize Python Project:
    *   [ ] Create directory structure: `/src` for code, `/tests` for unit tests
    *   [ ] Create basic `README.md` with project description and requirements
    *   [ ] Add `.gitignore` file for Python projects
*   [ ] Set up Virtual Environment:
    *   [ ] `python3 -m venv .venv`
    *   [ ] Document activation commands for different shells
*   [ ] Install Core Dependencies:
    *   [ ] Install PySide6 (`pip install PySide6`).
    *   [ ] Install Pillow (`pip install Pillow`).
*   [ ] Basic Git Repository Setup (`git init`, initial commit).

## Phase 2: Core Renaming Logic (`renamer_engine.py`)

*   [ ] Define basic renaming functions:
    *   [ ] `add_prefix_suffix(name, prefix, suffix)`
    *   [ ] `replace_substring(name, find, replace)`
    *   [ ] `change_case(name, case_option)` where case_option can be:
    *   "lower": Convert to lowercase
    *   "upper": Convert to UPPERCASE
    *   "title": Convert to Title Case
    *   "preserve": Keep original casing
    *   [ ] `format_number(number, padding, start, step)`
    *   [ ] `add_sequential_number(name, index, options)`
*   [ ] Implement `generate_preview_name(original_path, index, scheme_params)` function combining rules.
*   [ ] Implement `get_example_previews(file_list, scheme_params, count=5)` function using `generate_preview_name`.
*   [ ] Implement `check_conflicts_and_validity(file_list, scheme_params, destination_folder=None)`:
    *   [ ] Generate all potential new names/paths.
    *   [ ] Check for duplicate new names within the batch.
    *   [ ] Check for invalid filename characters (OS-specific).
    *   [ ] Check if proposed new name conflicts with an *existing* file (in source or destination dir).
    *   [ ] Return structured conflict report:
    *   `{ "duplicates": [], "invalid_chars": [], "existing_files": [] }`
    *   Include original/new paths for each conflict type
*   [ ] Implement `apply_rename(files_to_process, scheme_params, move_to_folder=None)`:
    *   [ ] Iterate through checked files (`files_to_process` should be list of tuples like `(original_path, index)`).
    *   [ ] Generate the final new name using `generate_preview_name`.
    *   [ ] Determine target path (original directory or `move_to_folder`).
    *   [ ] If `move_to_folder` is specified:
        *   [ ] Check if destination folder exists.
        *   [ ] Option/Logic to create destination folder if it doesn't exist.
        *   [ ] Perform `shutil.move(original_path, target_path)`.
    *   [ ] Else (rename in place):
        *   [ ] Perform `os.rename(original_path, target_path)`.
    *   [ ] Implement comprehensive error handling:
    *   `try...except` blocks for:
    *   `FileNotFoundError`, `PermissionError`, `FileExistsError`
    *   Custom exceptions for invalid naming patterns
    *   Detailed error logging with timestamps
    *   [ ] Return status for each file (Success, Error Type).

## Phase 3: GUI Implementation (`main.py` / `ui_module.py`)

*   **Main Window & Layout:**
    *   [ ] Create main application window (`QMainWindow`).
    *   [ ] Set up main layout structure (e.g., using `QSplitter` or `QHBoxLayout`/`QVBoxLayout`).
    *   [ ] Add placeholder areas/widgets for different sections.
*   **File System Tree View (Left Pane):**
    *   [ ] Implement `QTreeView`.
    *   [ ] Implement `QFileSystemModel` to populate the tree.
    *   [ ] Configure model filters (show directories only, or specific file types if needed).
    *   [ ] Set root path for the model (e.g., user's home directory).
    *   [ ] Connect `treeView.selectionModel().currentChanged` signal.
*   **Image Content View (Center Pane):**
    *   [ ] Implement `QListWidget`.
    *   [ ] Set `QListWidget` view mode to `QListView.IconMode`.
    *   [ ] Configure icon size and layout (grid size, spacing).
    *   [ ] Implement function `populate_image_view(folder_path)`:
        *   [ ] Clear existing items.
        *   [ ] Scan folder path for image files (use `os.listdir` or `glob`, filter by extension).
        *   [ ] For each image:
            *   [ ] Load image using Pillow (`Image.open`).
            *   [ ] Generate thumbnail (Pillow `thumbnail()` method).
            *   [ ] Convert Pillow thumbnail to `QPixmap`. (Requires care with image modes/formats).
            *   [ ] Create `QListWidgetItem` with filename text and thumbnail `QIcon`.
            *   [ ] Set item flags: `Qt.ItemIsSelectable`, `Qt.ItemIsEnabled`, `Qt.ItemIsUserCheckable`.
            *   [ ] Set initial check state to `Qt.Unchecked`.
            *   [ ] Add item to `QListWidget`.
    *   [ ] Call `populate_image_view` when a folder is selected in the `QTreeView`.
    *   [ ] Implement visual styling for *checked* items (e.g., background color change, border via Style Sheets).
    *   [ ] Add "Select All" / "Deselect All" buttons connected to list widget items.
    *   [ ] (Optional: Add detailed image preview panel):
    *   Show metadata (dimensions, format, size)
    *   Zoom/pan functionality for high-res images
    *   Side-by-side original/new name display
*   **Renaming Controls & Preview (Right/Bottom Pane):**
    *   [ ] Add input widgets (`QLineEdit`, `QSpinBox`, `QComboBox`, `QCheckBox`) for renaming schemes (Prefix, Suffix, Find, Replace, Numbering options, Case Change).
    *   [ ] Add `QTextEdit` or `QLabel`s area for the Example Preview.
    *   [ ] Add signal handlers for renaming control widgets (`textChanged`, `valueChanged`, etc.).
    *   [ ] Implement function `update_example_preview()`:
        *   [ ] Get current scheme parameters from UI controls.
        *   [ ] Get the first ~5 *checked* file paths (or first 5 files if none checked?).
        *   [ ] Call `renamer_engine.get_example_previews`.
        *   [ ] Display the examples in the preview area.
    *   [ ] Call `update_example_preview` when scheme controls change.
*   **Destination Folder Controls:**
    *   [ ] Add `QCheckBox` "Move renamed files to:".
    *   [ ] Add `QLineEdit` for destination path (disabled initially).
    *   [ ] Add "Browse..." `QPushButton` (disabled initially).
    *   [ ] Connect "Move" checkbox `toggled` signal to enable/disable path input and browse button.
    *   [ ] Implement "Browse..." button click handler using `QFileDialog.getExistingDirectory()`.
*   **Action Buttons & Status Bar:**
    *   [ ] Add "Rename Checked Files" `QPushButton`.
    *   [ ] Add `QProgressBar`.
    *   [ ] Add `QStatusBar` for messages.
    *   [ ] Implement "Rename" button click handler:
        *   [ ] Get list of *checked* items/paths from `QListWidget`.
        *   [ ] Get current scheme parameters from UI.
        *   [ ] Get destination folder path if "Move" is checked.
        *   [ ] Perform pre-rename check: Call `renamer_engine.check_conflicts_and_validity`.
        *   [ ] If conflicts/errors: Show warning message box and abort.
        *   [ ] Show confirmation dialog ("Rename N files? [Move to Y?] This cannot be easily undone.").
        *   [ ] If confirmed:
            *   [ ] Disable UI controls during rename.
            *   [ ] Call `renamer_engine.apply_rename` (potentially in a separate thread for responsiveness).
            *   [ ] Update progress bar based on progress reported from engine.
            *   [ ] Update item status visually in the list (e.g., icon change, text annotation) based on results.
            *   [ ] Show final summary in status bar/message box.
            *   [ ] Re-enable UI controls.
            *   [ ] Refresh the image view and potentially the file tree.

## Phase 4: Refinement & Packaging

*   [ ] **Error Handling:** Robustly handle file system errors, image loading errors, invalid user input.
*   [ ] **Performance Optimization:**
    *   Implement background threading for:
    *   Thumbnail generation (QThreadPool + QRunnable)
    *   File scanning operations
    *   Rename batch processing
    *   Add progress indicators for long operations
*   [ ] **Usability:** Refine UI layout, tooltips, labels. Ensure workflow is intuitive.
*   [ ] **Testing:** Test various renaming schemes, edge cases (empty folder, special characters, permissions).
*   [ ] **Documentation:**
    *   Code comments for all public functions/methods
    *   `README.md` with:
    *   Installation instructions
    *   Screenshots of GUI
    *   Usage examples with common renaming scenarios
    *   Troubleshooting common issues
*   [ ] **Packaging & Deployment:**
    *   [ ] Create platform-specific packages:
    *   Linux: `.deb` package with desktop integration
    *   Windows: Portable executable (PyInstaller)
    *   macOS: App bundle (py2app)
    *   [ ] Create `.desktop` file with:
    *   Proper MIME type associations
    *   Icon path specification
    *   Category matching Kubuntu's menu structure
    *   [ ] Implement update checking mechanism
