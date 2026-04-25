"""
LegalAssist - PyQt5 User Interface
Handles all GUI components and user interactions
"""

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QTextEdit, QPushButton, QLabel, QSizePolicy,
                             QMessageBox, QSplitter, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from logic import LegalLogicEngine


class MainWindow(QMainWindow):
    """Main Application Window"""

    def __init__(self):
        super().__init__()
        self.logic = LegalLogicEngine()
        self.init_ui()
        self.init_status_bar()

    def init_ui(self):
        """Initialize the user interface"""

        self.setWindowTitle("⚖️ LegalAssist - Legal Awareness System")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(600, 500)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(main_layout)

        # Title
        title = QLabel("⚖️ LegalAssist - Legal Awareness System")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2E7D32; padding: 10px;")
        main_layout.addWidget(title)

        # Disclaimer
        disclaimer = QLabel(
            "⚠️ DISCLAIMER: This is a legal awareness tool, NOT legal advice. "
            "Always consult a qualified lawyer for specific cases."
        )
        disclaimer.setStyleSheet(
            "background-color: #FFEBEE; color: #C62828; "
            "font-weight: bold; padding: 10px; border: 1px solid #EF9A9A;"
        )
        disclaimer.setAlignment(Qt.AlignCenter)
        disclaimer.setWordWrap(True)
        main_layout.addWidget(disclaimer)

        # Splitter
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ================= INPUT SECTION =================
        input_group = QGroupBox("📝 Describe Your Situation")
        input_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #2E7D32;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        input_layout = QVBoxLayout()
        input_group.setLayout(input_layout)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "Example: police ne roka aur parents ko call karne ko bola\n"
            "I am walking with my sister, both 18+, police stopped us and asked why we are together"
        )
        self.input_text.setFont(QFont("Arial", 11))
        self.input_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        input_layout.addWidget(self.input_text)

        # Analyze Button
        self.analyze_btn = QPushButton("🔍 Analyze Situation")
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 12px 30px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.analyze_btn.clicked.connect(self.analyze_input)

        input_layout.addWidget(self.analyze_btn)

        self.splitter.addWidget(input_group)

        # ================= OUTPUT SECTION =================
        output_group = QGroupBox("📋 Legal Awareness Output")
        output_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        output_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #1565C0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        output_layout = QVBoxLayout()
        output_group.setLayout(output_layout)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Arial", 11))
        self.output_text.setStyleSheet(
            "background-color: #F5F5F5; border: 1px solid #CCCCCC; border-radius: 5px;"
        )
        self.output_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        output_layout.addWidget(self.output_text)

        self.splitter.addWidget(output_group)

        # Give output more space
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)

        # Initial splitter sizes
        self.splitter.setSizes([250, 450])

        main_layout.addWidget(self.splitter, 1)

        main_layout.setStretch(2, 1)

        # Footer
        footer = QLabel("LegalAssist v1.0 | Offline Capable | Rule-Based System | © 2024")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #666666; padding: 5px; font-size: 10px;")
        main_layout.addWidget(footer)

    def init_status_bar(self):
        """Initialize status bar"""
        self.statusBar().showMessage("Ready - Enter your situation to begin")

    def analyze_input(self):
        """Analyze user input and display results"""

        user_text = self.input_text.toPlainText()

        if not user_text.strip():
            self.output_text.setText("⚠️ Please enter a description first.")
            self.statusBar().showMessage("Error: No input provided")
            return

        self.statusBar().showMessage("Analyzing...")
        QApplication.processEvents()

        try:
            signals = self.logic.detect_signals(user_text)
            matches = self.logic.match_situation(signals)
            response = self.logic.generate_response(user_text, matches)

            output_html = self.format_output(response)
            self.output_text.setHtml(output_html)

            if response['status'] == 'success':
                self.statusBar().showMessage(f"Analysis Complete: {response['situation']}")
            else:
                self.statusBar().showMessage("No specific situation detected")

        except Exception as e:
            self.output_text.setText(f"❌ Error: {str(e)}")
            self.statusBar().showMessage("Error during analysis")

    def format_output(self, data):
        """Format the output response as HTML"""

        if data['status'] == 'no_match':
            return f"""
            <div style="color: #666666; padding: 15px;">
                <p>{data['message']}</p>
                <p><i>Try describing your situation more clearly with keywords like: police, stop, harassment, parents, etc.</i></p>
            </div>
            """

        html = f"""
        <div style="padding: 15px;">
        <h2 style="color: #2E7D32; border-bottom: 2px solid #2E7D32;">
        📌 Situation: {data['situation']}
        </h2>

        <p><b>Confidence Level:</b> {data['confidence']}</p>
        <p style="color:#1565C0;">{data['guidance']}</p>
        """

        if 'general_guidance' in data and data['general_guidance']:
            html += f"""
            <h3 style="color:#6A1B9A;">🧭 General Guidance:</h3>
            <p>{data['general_guidance']}</p>
            """

        html += """
        <h3 style="color:#1565C0;">📚 Applicable Laws:</h3>
        <ul>
        """

        for law in data['laws']:
            html += f"""
            <li>
            <b>{law['type']} - {law['section']}</b><br>
            <i>{law['title']}</i><br>
            {law['explanation']}
            </li>
            """

        html += """
        </ul>
        </div>
        """

        return html