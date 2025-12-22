# -*- coding: utf-8 -*-
"""
setup.py - PyInstaller Configuration for LegalAssist
Builds standalone .exe and app bundles
"""

import sys
from PyInstaller.utils.hooks import collect_all

# Package metadata
name = 'LegalAssist'
version = '1.0.0'
author = 'LegalAssist Team'
description = 'Legal Awareness System for Indian Citizens'

# Data to include
datas = [
    ('data', 'data'),           # JSON data files
    ('ui', 'ui'),               # UI module
    ('engine', 'engine'),       # Engine module
]

# Build configuration
if sys.platform == 'win32':
    # Windows .exe build
    import PyInstaller.building.build_main as build_main
    
    build_exe_options = {
        'packages': ['PyQt5'],
        'include_files': datas,
        'icon': 'icon.ico' if Path('icon.ico').exists() else None,
    }
elif sys.platform == 'darwin':
    # macOS app build
    app_options = {
        'packages': ['PyQt5'],
        'include_files': datas,
    }

# To build: python setup.py py2exe (Windows) or py2app (macOS)
# Or use: pyinstaller legalassist.spec
