#!/usr/bin/env python3
"""
LegalAssist - Legal Awareness System
Entry Point for PyQt Desktop Application
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("LegalAssist")
    app.setOrganizationName("LegalAssist")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()