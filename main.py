"""
main.py - LegalAssist: Complete Legal Awareness System for India
Modern PyQt5 application with professional dark theme and intuitive UI
"""

import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont

from engine.matcher import LegalAssistMatcher
from engine.normalizer import Normalizer
from ui.styles import MAIN_STYLESHEET, STATUS_COLORS
from ui.components import ResultCard, LawWidget, DisclaimerWidget


class LegalAssistApp(QMainWindow):
    """Main application window with polished, organized UI"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LegalAssist - Know Your Rights ⚖️")
        
        # Set window size and position
        self.resize(1000, 800)
        self.setMinimumSize(900, 700)
        
        # Center window on screen
        self.center_window()
        
        # Initialize data
        self.load_data()
        
        if self.data_loaded:
            self.init_ui()
            self.apply_styles()
        else:
            self.show_error_window()
    
    def center_window(self):
        """Center the window on the screen"""
        try:
            from PyQt5.QtWidgets import QApplication
            screen_geometry = QApplication.primaryScreen().geometry()
            window_geometry = self.frameGeometry()
            
            center_x = (screen_geometry.width() - window_geometry.width()) // 2
            center_y = (screen_geometry.height() - window_geometry.height()) // 2
            
            self.move(max(0, center_x), max(0, center_y))
        except:
            # If centering fails, just position at top-left
            self.move(100, 100)
    
    def load_data(self):
        """Load JSON data files with UTF-8 encoding"""
        try:
            data_dir = Path(__file__).parent / 'data'
            
            # Load JSON files with UTF-8 encoding for Hindi/Unicode support
            with open(data_dir / 'keywords.json', encoding='utf-8') as f:
                self.keywords = json.load(f)
            
            with open(data_dir / 'situations.json', encoding='utf-8') as f:
                self.situations = json.load(f)
            
            with open(data_dir / 'laws.json', encoding='utf-8') as f:
                self.laws = json.load(f)
            
            self.data_loaded = True
            print(f"✅ Data loaded: {len(self.keywords)} keywords, {len(self.situations)} situations, {len(self.laws)} laws")
            
            # Initialize matcher
            self.matcher = LegalAssistMatcher(self.keywords, self.situations, self.laws)
            self.normalizer = Normalizer()
        
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.data_loaded = False
    
    def init_ui(self):
        """Initialize polished and organized UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with padding
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # ===== HEADER SECTION =====
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        # Title
        title = QLabel("⚖️ LegalAssist")
        title_font = QFont("Arial", 24, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2196F3;")
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Understand Your Legal Rights in Simple Language")
        subtitle_font = QFont("Arial", 12)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #999999;")
        header_layout.addWidget(subtitle)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #444444;")
        header_layout.addWidget(separator)
        
        main_layout.addLayout(header_layout)
        
        # ===== RESULTS SECTION (FIRST - TOP) =====
        results_label = QLabel("📋 Results")
        results_label_font = QFont("Arial", 11, QFont.Bold)
        results_label.setFont(results_label_font)
        results_label.setStyleSheet("color: #2196F3;")
        main_layout.addWidget(results_label)
        
        # Scrollable results area
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: 1px solid #444444;
                border-radius: 8px;
            }
            QScrollBar:vertical {
                background-color: #1e1e1e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #444444;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #555555;
            }
        """)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(300)  # Large height
        
        # Results container
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_layout.setContentsMargins(10, 10, 10, 10)
        self.results_layout.setSpacing(12)
        
        # Placeholder message
        self.placeholder = QLabel("Enter a situation below and click 'Check Situation' to see results here")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setWordWrap(True)
        self.placeholder.setStyleSheet("color: #666666; font-size: 13px;")
        self.placeholder.setMinimumHeight(200)
        self.results_layout.addWidget(self.placeholder)
        
        self.results_layout.addStretch()
        self.results_container.setLayout(self.results_layout)
        self.scroll_area.setWidget(self.results_container)
        
        main_layout.addWidget(self.scroll_area, 3)  # Takes 3x space
        
        # ===== INPUT SECTION (SECOND - BOTTOM) =====
        input_section_layout = QVBoxLayout()
        input_section_layout.setSpacing(10)
        
        # Input label with icon
        input_label = QLabel("📝 Describe Your Situation")
        input_label_font = QFont("Arial", 11, QFont.Bold)
        input_label.setFont(input_label_font)
        input_label.setStyleSheet("color: #2196F3;")
        input_section_layout.addWidget(input_label)
        
        # Input text area with improved styling
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText(
            "Enter your legal situation in English, Hindi, or Hinglish...\n\n"
            "Examples:\n"
            "• 'Police stopped me without reason'\n"
            "• 'Police ne roka aur gaali diye'\n"
            "• 'पुलिस ने रोका'"
        )
        self.input_field.setMinimumHeight(100)
        self.input_field.setMaximumHeight(130)
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #444444;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                font-family: Arial;
            }
            QTextEdit:focus {
                border: 2px solid #2196F3;
            }
        """)
        input_section_layout.addWidget(self.input_field)
        
        # Button layout (horizontal)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Check Situation button
        self.check_btn = QPushButton("🔍 Check Situation")
        self.check_btn.setMinimumHeight(42)
        self.check_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.check_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.check_btn.clicked.connect(self.check_situation)
        button_layout.addWidget(self.check_btn)
        
        # Clear button
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.setMinimumHeight(42)
        self.clear_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_input)
        button_layout.addWidget(self.clear_btn)
        
        button_layout.addStretch()
        input_section_layout.addLayout(button_layout)
        
        main_layout.addLayout(input_section_layout, 1)  # Takes 1x space
        
        # ===== FOOTER SECTION =====
        footer = QLabel("LegalAssist v1.0.0 • Made for Legal Awareness in India • Know Your Rights ⚖️")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #666666; font-size: 10px; margin-top: 10px;")
        main_layout.addWidget(footer)
        
        central_widget.setLayout(main_layout)
    
    def apply_styles(self):
        """Apply stylesheet to main window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }
        """)
    
    def check_situation(self):
        """Process user input and display results"""
        user_input = self.input_field.toPlainText().strip()
        
        if not user_input:
            self.show_placeholder("Please enter a situation to analyze")
            return
        
        try:
            # Process query
            result = self.matcher.process_query(user_input)
            matches = result.get('matches', [])
            
            # Clear previous results
            while self.results_layout.count() > 0:
                item = self.results_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            if not matches:
                self.show_placeholder("No matching situations found. Please try a different description.")
                return
            
            # Display results
            self.placeholder.hide()
            
            for match in matches:
                # Result card
                card = ResultCard()
                card.populate(match)
                self.results_layout.addWidget(card)
                
                # Laws section
                if match.get('laws'):
                    laws_label = QLabel("📜 Applicable Laws:")
                    laws_label.setStyleSheet("color: #2196F3; font-weight: bold; margin-top: 8px;")
                    self.results_layout.addWidget(laws_label)
                    
                    for law in match['laws']:
                        law_widget = LawWidget()
                        law_widget.populate(law)
                        self.results_layout.addWidget(law_widget)
                
                # What you can ask section
                if match.get('what_you_can_ask'):
                    ask_label = QLabel("❓ Questions You Can Ask:")
                    ask_label.setStyleSheet("color: #4CAF50; font-weight: bold; margin-top: 8px;")
                    self.results_layout.addWidget(ask_label)
                    
                    for question in match['what_you_can_ask']:
                        q_label = QLabel(f"• {question}")
                        q_label.setWordWrap(True)
                        q_label.setStyleSheet("color: #cccccc; margin-left: 12px; font-size: 12px;")
                        self.results_layout.addWidget(q_label)
                
                # Separator
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setStyleSheet("color: #333333; margin: 12px 0;")
                self.results_layout.addWidget(sep)
            
            self.results_layout.addStretch()
        
        except Exception as e:
            self.show_placeholder(f"Error processing query: {str(e)}")
    
    def clear_input(self):
        """Clear input field and reset results"""
        self.input_field.clear()
        self.show_placeholder("Enter a situation below and click 'Check Situation' to see results here")
    
    def show_placeholder(self, message):
        """Show placeholder message in results area"""
        # Clear results
        while self.results_layout.count() > 0:
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Show placeholder
        self.placeholder = QLabel(message)
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setWordWrap(True)
        self.placeholder.setStyleSheet("color: #666666; font-size: 13px;")
        self.placeholder.setMinimumHeight(200)
        self.results_layout.addWidget(self.placeholder)
        self.results_layout.addStretch()
    
    def show_error_window(self):
        """Show error if data failed to load"""
        error_label = QLabel("❌ Failed to load application data.\nPlease check that all JSON files are present and valid.")
        error_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(error_label)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Application metadata
    app.setApplicationName("LegalAssist")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = LegalAssistApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()