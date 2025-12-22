"""
styles.py - Modern PyQt5 styling and theme
Professional, accessible, dark-mode friendly
"""

# Color scheme
COLORS = {
    'primary': '#2196F3',      # Blue
    'primary_hover': '#1976D2',
    'success': '#4CAF50',      # Green
    'warning': '#FF9800',      # Orange
    'danger': '#F44336',       # Red
    'info': '#00BCD4',         # Cyan
    
    'bg_dark': '#1e1e1e',      # Dark background
    'bg_light': '#f5f5f5',     # Light background
    'surface_dark': '#2d2d2d',
    'surface_light': '#ffffff',
    
    'text_dark': '#ffffff',
    'text_light': '#333333',
    'text_secondary': '#999999',
    
    'border': '#444444',
}

# Main stylesheet
MAIN_STYLESHEET = """
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
}

QLabel {
    color: #ffffff;
    font-size: 13px;
}

QLineEdit, QTextEdit {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 8px;
    font-size: 13px;
    selection-background-color: #2196F3;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #2196F3;
}

QPushButton {
    background-color: #2196F3;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: bold;
    margin: 5px;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #1565C0;
}

QPushButton:disabled {
    background-color: #666666;
    color: #999999;
}

QScrollArea {
    background-color: #1e1e1e;
    border: none;
}

QFrame {
    background-color: #2d2d2d;
    border: 1px solid #444444;
    border-radius: 4px;
}

QTabWidget::pane {
    border: 1px solid #444444;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #ffffff;
    padding: 6px 16px;
    border: 1px solid #444444;
}

QTabBar::tab:selected {
    background-color: #2196F3;
    color: #ffffff;
}

QComboBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 5px;
}

QComboBox::drop-down {
    border: none;
}

QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 12px;
}

QScrollBar::handle:vertical {
    background-color: #444444;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #666666;
}

QMessageBox {
    background-color: #1e1e1e;
}

QMessageBox QLabel {
    color: #ffffff;
}

QMessageBox QPushButton {
    min-width: 60px;
}
"""

# Cards and containers
CARD_STYLESHEET = """
QFrame {
    background-color: #2d2d2d;
    border: 1px solid #444444;
    border-radius: 8px;
    padding: 12px;
    margin: 6px;
}
"""

# Success/Warning/Error colors
STATUS_COLORS = {
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'info': '#2196F3',
}

def get_status_stylesheet(status: str) -> str:
    """Get stylesheet for status indicators"""
    color = STATUS_COLORS.get(status, STATUS_COLORS['info'])
    return f"""
    QLabel {{
        color: {color};
        font-weight: bold;
    }}
    """
