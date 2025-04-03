"""
GUI implementation using PySide6
"""
import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QSplitter, QTreeView, 
                               QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QGroupBox, QCheckBox, QLineEdit,
                               QSpinBox, QComboBox, QProgressBar, QStatusBar,
                               QFileDialog, QMessageBox, QFileSystemModel,
                               QSizePolicy)
from PySide6.QtCore import Qt, QSize, QDir
from PySide6.QtGui import QPixmap, QIcon
from PIL import Image, ImageQt

# Import renamer engine functions
from renamer_engine import (
    get_example_previews, 
    check_conflicts_and_validity, 
    apply_rename
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Main window setup
        self.setWindowTitle("Kubuntu Image Batch Renamer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main splitter for three panes
        self.main_splitter = QSplitter(Qt.Horizontal)
        
        # File system tree view (left pane)
        self.file_tree = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_tree.setModel(self.file_model)
        
        # Image content view (center pane)
        self.image_container = QWidget()
        self.image_layout = QVBoxLayout(self.image_container)
        
        # Create image list with Dolphin file manager style
        self.image_list = QListWidget()
        self.image_list.setViewMode(QListWidget.IconMode)
        self.image_list.setIconSize(QSize(96, 96))         # Slightly smaller icons like Dolphin
        self.image_list.setResizeMode(QListWidget.Adjust)  # Allow items to adjust with resize
        self.image_list.setMovement(QListWidget.Static)    # Prevent items from being moved
        self.image_list.setFlow(QListWidget.LeftToRight)   # Flow items from left to right
        self.image_list.setWrapping(True)                  # Wrap to next row when needed
        self.image_list.setSpacing(10)                     # Space between items like Dolphin
        self.image_list.setUniformItemSizes(True)          # All items same size for better performance
        self.image_list.setMinimumSize(500, 400)           # Prevent shrinking below usable size
        self.image_list.setSelectionMode(QListWidget.MultiSelection)
        self.image_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.image_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Dolphin-style grid layout
        self.image_list.setGridSize(QSize(120, 130))       # Compact grid size similar to Dolphin
        
        # Selection buttons
        self.selection_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.deselect_all_btn = QPushButton("Deselect All")
        
        self.selection_layout.addWidget(self.select_all_btn)
        self.selection_layout.addWidget(self.deselect_all_btn)
        
        # Add to layout
        self.image_layout.addWidget(self.image_list)
        self.image_layout.addLayout(self.selection_layout)
        
        # Connect buttons
        self.select_all_btn.clicked.connect(self.select_all_images)
        self.deselect_all_btn.clicked.connect(self.deselect_all_images)
        self.image_list.itemSelectionChanged.connect(self.update_preview)
        
        # Set custom styles for the image list with light blue text and larger font
        self.image_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                font-size: 11pt;  /* Larger font size */
            }
            QListWidget::item {
                border: 2px solid #ff0000;  /* Reduced red border for unselected items */
                border-radius: 3px;
                padding: 3px;
                margin: 1px;
                background-color: transparent;  /* Transparent background */
                color: #4682B4;  /* Steel blue text color */
                font-weight: bold;  /* Make text bold for better visibility */
            }
            QListWidget::item:selected {
                border: 2px solid #00ff00;  /* Reduced green border for selected items */
                background-color: rgba(0, 255, 0, 0.1);  /* Light green background */
                color: #1E90FF;  /* Dodger blue for selected items */
            }
            /* Make text background transparent */
            QListWidget::item:!active:!selected {
                background: transparent;
            }
        """)
        
        # Customize the list widget to improve text display
        self.image_list.setTextElideMode(Qt.ElideRight)  # Use ellipsis for text that doesn't fit
        
        # Renaming controls (right pane)
        self.controls_pane = QWidget()
        
        # Add widgets to splitter
        self.main_splitter.addWidget(self.file_tree)
        self.main_splitter.addWidget(self.image_container)
        self.main_splitter.addWidget(self.controls_pane)
        
        # Set splitter sizes
        self.main_splitter.setSizes([300, 600, 300])
        
        # Create layouts
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.main_splitter)
        
        # Setup file system tree
        self.setup_file_tree()
        
        # Setup image list view
        self.setup_image_list()
        
        # Setup controls pane
        self.setup_controls_pane()
        
        # Setup status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
    def setup_file_tree(self):
        """Setup the file system tree view"""
        # Set file model properties
        self.file_model.setRootPath(QDir.homePath())
        self.file_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files)
        
        # Set name filters for image files
        self.file_model.setNameFilters(["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff"])
        self.file_model.setNameFilterDisables(False)  # Hide filtered files instead of disabling them
        
        # Set tree view properties
        self.file_tree.setRootIndex(self.file_model.index(QDir.homePath()))
        self.file_tree.setHeaderHidden(True)
        self.file_tree.hideColumn(1)  # Size
        self.file_tree.hideColumn(2)  # Type
        self.file_tree.hideColumn(3)  # Modified
        
        # Connect selection changed signal
        self.file_tree.selectionModel().currentChanged.connect(self.on_folder_selected)
        
    def setup_image_list(self):
        """This method is now a placeholder since image list setup is done in init_ui"""
        pass
        
    def setup_controls_pane(self):
        """Setup the renaming controls pane"""
        controls_layout = QVBoxLayout(self.controls_pane)
        
        # Name Template Group
        name_group = QGroupBox("Name Template")
        name_layout = QVBoxLayout(name_group)
        
        name_input_layout = QHBoxLayout()
        name_input_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name pattern (e.g., photo)")
        self.name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.name_input.setMaximumWidth(300)  # Limit the maximum width
        name_input_layout.addWidget(self.name_input)
        
        name_layout.addLayout(name_input_layout)
        
        # Add a note explaining that extensions are preserved
        ext_note = QLabel("Note: File extensions will be automatically preserved.")
        ext_note.setStyleSheet("font-size: 10px; color: gray;")
        name_layout.addWidget(ext_note)
        
        # Find/Replace Group
        find_replace_group = QGroupBox("Find/Replace")
        find_replace_layout = QVBoxLayout(find_replace_group)
        
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input)
        
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input)
        
        find_replace_layout.addLayout(find_layout)
        find_replace_layout.addLayout(replace_layout)
        
        # Case Change Group
        case_group = QGroupBox("Case")
        case_layout = QHBoxLayout(case_group)
        self.case_combo = QComboBox()
        self.case_combo.addItems(["Preserve", "lowercase", "UPPERCASE", "Title Case"])
        case_layout.addWidget(QLabel("Change case:"))
        case_layout.addWidget(self.case_combo)
        
        # Numbering Group
        numbering_group = QGroupBox("Sequential Numbers")
        numbering_layout = QVBoxLayout(numbering_group)
        
        self.use_numbering = QCheckBox("Add sequential numbers")
        numbering_layout.addWidget(self.use_numbering)
        
        number_options_layout = QHBoxLayout()
        
        number_options_layout.addWidget(QLabel("Start:"))
        self.number_start = QSpinBox()
        self.number_start.setValue(1)
        number_options_layout.addWidget(self.number_start)
        
        number_options_layout.addWidget(QLabel("Padding:"))
        self.number_padding = QSpinBox()
        self.number_padding.setValue(2)
        self.number_padding.setMinimum(1)
        self.number_padding.setMaximum(10)
        number_options_layout.addWidget(self.number_padding)
        
        numbering_layout.addLayout(number_options_layout)
        
        # Destination Group
        destination_group = QGroupBox("Destination")
        destination_layout = QVBoxLayout(destination_group)
        
        self.move_files = QCheckBox("Move files to:")
        destination_layout.addWidget(self.move_files)
        
        dest_path_layout = QHBoxLayout()
        self.dest_path = QLineEdit()
        self.dest_path.setEnabled(False)
        dest_path_layout.addWidget(self.dest_path)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setEnabled(False)
        dest_path_layout.addWidget(self.browse_btn)
        
        destination_layout.addLayout(dest_path_layout)
        
        # Preview Group that expands to fill available space
        preview_group = QGroupBox("Preview")
        preview_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow vertical expansion
        preview_layout = QVBoxLayout(preview_group)
        
        # Create a scrollable area for the preview to contain long filenames
        from PySide6.QtWidgets import QScrollArea
        preview_scroll = QScrollArea()
        preview_scroll.setWidgetResizable(True)
        preview_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        preview_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        preview_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow vertical expansion
        
        # Create a widget to hold our preview label
        preview_content = QWidget()
        preview_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow vertical expansion
        preview_content_layout = QVBoxLayout(preview_content)
        
        # Create the preview label with word wrapping
        self.preview_label = QLabel("No files selected")
        self.preview_label.setWordWrap(True)  # Enable word wrapping for long filenames
        self.preview_label.setTextFormat(Qt.RichText)  # Use rich text for formatting
        self.preview_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Align text to top-left
        
        # Add the label to the content layout
        preview_content_layout.addWidget(self.preview_label)
        preview_content_layout.addStretch()
        
        # Set the content widget in the scroll area
        preview_scroll.setWidget(preview_content)
        
        # Add the scroll area to the preview layout
        preview_layout.addWidget(preview_scroll)
        
        # Confirmation option and action buttons
        confirmation_layout = QHBoxLayout()
        self.skip_confirmation = QCheckBox("Skip confirmation")
        confirmation_layout.addWidget(self.skip_confirmation)
        confirmation_layout.addStretch()  # Push buttons to the right
        
        # Action Buttons
        action_layout = QHBoxLayout()
        self.rename_btn = QPushButton("Rename Files")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        action_layout.addWidget(self.rename_btn)
        action_layout.addWidget(self.progress_bar)
        
        # Add all groups to main controls layout with proper sizing
        # Fixed-size groups at the top
        controls_layout.addWidget(name_group)
        controls_layout.addWidget(find_replace_group)
        controls_layout.addWidget(case_group)
        controls_layout.addWidget(numbering_group)
        controls_layout.addWidget(destination_group)
        
        # Expandable preview in the middle
        controls_layout.addWidget(preview_group, 1)  # Give it a stretch factor of 1 to fill available space
        
        # Add confirmation option
        controls_layout.addLayout(confirmation_layout)
        
        # Action buttons at the bottom
        controls_layout.addLayout(action_layout)
        
        # Connect signals
        self.move_files.toggled.connect(self.toggle_destination)
        self.browse_btn.clicked.connect(self.browse_destination)
        self.rename_btn.clicked.connect(self.rename_files)
        
        # Connect renaming control signals to update preview
        self.name_input.textChanged.connect(self.update_preview)
        self.find_input.textChanged.connect(self.update_preview)
        self.replace_input.textChanged.connect(self.update_preview)
        self.case_combo.currentIndexChanged.connect(self.update_preview)
        self.use_numbering.toggled.connect(self.update_preview)
        self.number_start.valueChanged.connect(self.update_preview)
        self.number_padding.valueChanged.connect(self.update_preview)
    
    def on_folder_selected(self, current, previous):
        """Handle folder selection in the file tree"""
        if current.isValid():
            path = self.file_model.filePath(current)
            print(f"Selected path: {path}")
            self.statusBar.showMessage(f"Selected path: {path}")
            
            # Only try to load images if the selected path is a directory
            if os.path.isdir(path):
                print(f"Loading images from directory: {path}")
                self.populate_image_view(path)
            else:
                print(f"Not a directory: {path}")
    
    def populate_image_view(self, folder_path):
        """Populate the image list with thumbnails from the selected folder"""
        # Clear existing items
        self.image_list.clear()
        
        print(f"Clearing image list and starting to load images from: {folder_path}")
        self.statusBar.showMessage(f"Loading images from {folder_path}...")
        
        # Update the UI (process pending events)
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.processEvents()
        
        # Get list of image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        
        try:
            # Get all files in the directory
            all_files = os.listdir(folder_path)
            print(f"Found {len(all_files)} total files in directory")
            
            # Filter for image files only
            files = []
            for f in all_files:
                if (os.path.isfile(os.path.join(folder_path, f)) and 
                    os.path.splitext(f.lower())[1] in image_extensions):
                    files.append(f)
            
            print(f"Found {len(files)} image files to load")
            
            # Sort files
            files.sort()
            
            # Limit the number of images to load (to prevent freezing with large folders)
            max_images = 100
            if len(files) > max_images:
                print(f"Limiting to {max_images} images instead of {len(files)}")
                files = files[:max_images]
            
            # Add images to list widget
            for i, filename in enumerate(files):
                if i % 10 == 0:
                    # Update status every 10 images
                    self.statusBar.showMessage(f"Loading image {i+1} of {len(files)}...")
                    QCoreApplication.processEvents()  # Update UI
                
                file_path = os.path.join(folder_path, filename)
                try:
                    # Create a placeholder for images that fail to load
                    try:
                        # Load image and create thumbnail
                        image = Image.open(file_path)
                        image.thumbnail((128, 128))
                        
                        # Convert PIL image to QPixmap
                        qim = ImageQt.ImageQt(image)
                        pixmap = QPixmap.fromImage(qim)
                    except Exception as e:
                        print(f"Error creating thumbnail for {filename}: {str(e)}")
                        # Create a placeholder icon
                        pixmap = QPixmap(128, 128)
                        pixmap.fill(Qt.red)  # Fill with red color to indicate error
                    
                    icon = QIcon(pixmap)
                    
                    # Create list item with improved display
                    item = QListWidgetItem(icon, filename)
                    item.setFlags(item.flags() | Qt.ItemIsSelectable)
                    item.setData(Qt.UserRole, file_path)  # Store full path
                    
                    # Set a fixed size for the item that's large enough for the icon but not too large
                    # This helps prevent the text from taking up too much space
                    item.setSizeHint(QSize(140, 160))  # Width: icon + small padding, Height: icon + space for text
                    
                    # Display shortened text below the image (Dolphin style)
                    # Also keep tooltip for full filename
                    if len(filename) > 14:
                        display_name = filename[:11] + "..."
                        item.setText(display_name)
                    else:
                        item.setText(filename)
                    item.setToolTip(filename)
                    
                    # Apply the blue text color defined in the stylesheet
                    # The color is already set in the stylesheet, so we don't need to set it here
                    
                    self.image_list.addItem(item)
                    
                    # Process events periodically to keep UI responsive
                    if i % 5 == 0:
                        QCoreApplication.processEvents()
                        
                except Exception as e:
                    print(f"Error adding item for {filename}: {str(e)}")
            
            print(f"Successfully loaded {self.image_list.count()} images")
            self.statusBar.showMessage(f"Loaded {self.image_list.count()} images from {folder_path}")
        except Exception as e:
            print(f"Error loading folder: {str(e)}")
            self.statusBar.showMessage(f"Error loading folder: {str(e)}")
    
    def select_all_images(self):
        """Select all images in the list"""
        self.image_list.selectAll()
        self.update_preview()
    
    def deselect_all_images(self):
        """Deselect all images in the list"""
        self.image_list.clearSelection()
        self.update_preview()
    
    def toggle_image_selection(self, item):
        """Toggle selection state when an image is clicked"""
        # Toggle the selection state
        item.setSelected(not item.isSelected())
        self.update_preview()
    
    def toggle_destination(self, checked):
        """Enable/disable destination controls"""
        self.dest_path.setEnabled(checked)
        self.browse_btn.setEnabled(checked)
    
    def browse_destination(self):
        """Open file dialog to select destination folder"""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Destination Folder", QDir.homePath()
        )
        if folder:
            self.dest_path.setText(folder)
    
    def get_scheme_params(self):
        """Get the current renaming scheme parameters from UI controls"""
        params = {
            "replace_name": True if self.name_input.text() else False,  # Flag to indicate if we should replace the entire name
            "new_name": self.name_input.text(),  # New name to use if replacing
            "prefix": "",  # We're not using prefix anymore
            "suffix": "",  # Empty suffix
            "find": self.find_input.text(),
            "replace": self.replace_input.text(),
            "case_option": self.case_combo.currentText().lower(),
            "use_numbering": self.use_numbering.isChecked(),
            "number_options": {
                "padding": self.number_padding.value(),
                "start": self.number_start.value(),
                "step": 1,
                "position": "suffix",
                "separator": "_"
            }
        }
        return params
    
    def get_checked_files(self):
        """Get list of selected file paths"""
        selected_files = []
        for item in self.image_list.selectedItems():
            file_path = item.data(Qt.UserRole)
            selected_files.append(file_path)
        return selected_files
    
    def update_preview(self):
        """Update the renaming preview"""
        # Get checked files
        checked_files = self.get_checked_files()
        
        if not checked_files:
            self.preview_label.setText("No files selected")
            return
        
        # Get renaming scheme parameters
        scheme_params = self.get_scheme_params()
        
        # Generate previews using the renamer engine
        previews = get_example_previews(checked_files, scheme_params, 5)
        
        # Format the preview HTML with truncated filenames
        preview_text = f"<b>{len(checked_files)} files selected</b><br>"
        preview_text += "<table style='margin-top: 10px; max-width: 280px;'>"
        preview_text += "<tr><th>Original</th><th>New Name</th></tr>"
        
        for original, preview in previews:
            # Truncate long filenames for display
            orig_display = original
            preview_display = preview
            
            if len(original) > 20:
                orig_display = original[:17] + "..."
            
            if len(preview) > 20:
                preview_display = preview[:17] + "..."
            
            # Add tooltip with full names
            preview_text += f"<tr><td title='{original}'>{orig_display}</td><td title='{preview}'>{preview_display}</td></tr>"
        
        if len(checked_files) > 5:
            preview_text += f"<tr><td colspan='2'>... and {len(checked_files) - 5} more files</td></tr>"
        
        preview_text += "</table>"
        
        self.preview_label.setText(preview_text)
    
    def rename_files(self):
        """Rename the selected files"""
        # Store the current directory path before renaming
        current_dir = os.path.dirname(self.get_checked_files()[0]) if self.get_checked_files() else None
        
        # Get checked files and their indices
        checked_files = self.get_checked_files()
        
        if not checked_files:
            QMessageBox.warning(self, "No Files Selected", 
                                "Please select files to rename first.")
            return
        
        # Get renaming scheme parameters
        scheme_params = self.get_scheme_params()
        
        # Get destination folder if moving
        move_to_folder = None
        if self.move_files.isChecked():
            move_to_folder = self.dest_path.text()
            if not move_to_folder:
                QMessageBox.warning(self, "No Destination", 
                                    "Please select a destination folder.")
                return
        
        # Check for conflicts and validity issues
        conflict_report = check_conflicts_and_validity(
            checked_files, scheme_params, move_to_folder
        )
        
        # Check if there are any issues
        has_issues = any(len(issues) > 0 for issues in conflict_report.values())
        
        if has_issues:
            # Format the conflict message
            conflict_msg = "The following issues were found:\n\n"
            
            if conflict_report["duplicates"]:
                conflict_msg += "Duplicate new names:\n"
                for path, name in conflict_report["duplicates"][:5]:
                    conflict_msg += f"- {os.path.basename(path)} → {name}\n"
                if len(conflict_report["duplicates"]) > 5:
                    conflict_msg += f"... and {len(conflict_report['duplicates']) - 5} more\n"
                conflict_msg += "\n"
            
            if conflict_report["invalid_chars"]:
                conflict_msg += "Names with invalid characters:\n"
                for path, name in conflict_report["invalid_chars"][:5]:
                    conflict_msg += f"- {os.path.basename(path)} → {name}\n"
                if len(conflict_report["invalid_chars"]) > 5:
                    conflict_msg += f"... and {len(conflict_report['invalid_chars']) - 5} more\n"
                conflict_msg += "\n"
            
            if conflict_report["existing_files"]:
                conflict_msg += "Would overwrite existing files:\n"
                for path, name in conflict_report["existing_files"][:5]:
                    conflict_msg += f"- {os.path.basename(path)} → {name}\n"
                if len(conflict_report["existing_files"]) > 5:
                    conflict_msg += f"... and {len(conflict_report['existing_files']) - 5} more\n"
                conflict_msg += "\n"
            
            conflict_msg += "Please modify your renaming settings and try again."
            
            # Show conflict warning
            QMessageBox.warning(self, "Renaming Issues", conflict_msg)
            return
        
        # Show confirmation dialog if not skipped
        if not self.skip_confirmation.isChecked():
            action = "Move" if move_to_folder else "Rename"
            destination = f" to {move_to_folder}" if move_to_folder else ""
            
            confirm_msg = f"{action} {len(checked_files)} files{destination}?\n\n"
            confirm_msg += "This operation cannot be easily undone."
            
            reply = QMessageBox.question(self, "Confirm Rename", confirm_msg,
                                         QMessageBox.Yes | QMessageBox.No)
            
            if reply != QMessageBox.Yes:
                return
        
        # Prepare files to process (with indices)
        files_to_process = [(path, i) for i, path in enumerate(checked_files)]
        
        # Disable UI during operation
        self.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(files_to_process))
        self.progress_bar.setValue(0)
        
        # Apply renaming
        result = apply_rename(files_to_process, scheme_params, move_to_folder)
        
        # Update UI and show result in status bar only (no popup)
        self.progress_bar.setValue(len(files_to_process))
        self.statusBar.showMessage(result["message"])
        
        # Re-enable UI
        self.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Determine which directory to refresh
        refresh_directory = move_to_folder if move_to_folder else current_dir
        
        # Refresh the view using the appropriate directory
        if refresh_directory:
            # Update the file tree selection to match the directory we're refreshing
            index = self.file_model.index(refresh_directory)
            self.file_tree.setCurrentIndex(index)
            
            # Populate the image view with the refreshed directory content
            self.populate_image_view(refresh_directory)
