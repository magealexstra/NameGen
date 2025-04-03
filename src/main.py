#!/usr/bin/env python3
"""
Kubuntu Image Batch Renamer
Main application entry point
"""
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDir
from ui_module import MainWindow

def main():
    """
    Application entry point
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Kubuntu Image Batch Renamer")
    app.setOrganizationName("KubuntuApps")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # For testing: Directly load the Pictures folder if it exists
    pictures_path = os.path.join(QDir.homePath(), "Pictures")
    if os.path.exists(pictures_path) and os.path.isdir(pictures_path):
        from PySide6.QtCore import QTimer
        QTimer.singleShot(500, lambda: window.populate_image_view(pictures_path))
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
