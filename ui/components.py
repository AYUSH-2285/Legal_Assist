"""
components.py - Reusable PyQt5 components
Cards, buttons, headers, result displays
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ResultCard(QFrame):
    """
    Card component for displaying a legal situation match result
    Shows: Situation name, confidence score, applicable laws
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 2px solid #444444;
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(8)
        
        # Header
        self.header_layout = QHBoxLayout()
        
        self.title = QLabel()
        self.title.setFont(QFont("Arial", 12, QFont.Bold))
        self.title.setStyleSheet("color: #2196F3;")
        
        self.confidence = QLabel()
        self.confidence.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.header_layout.addWidget(self.title)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.confidence)
        
        self.layout.addLayout(self.header_layout)
        
        # Description
        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setStyleSheet("color: #cccccc; font-size: 11px;")
        self.layout.addWidget(self.description)
        
        # Severity badge
        self.severity = QLabel()
        self.severity.setStyleSheet("color: #FF9800; font-weight: bold;")
        self.layout.addWidget(self.severity)
    
    def populate(self, situation_data: dict):
        """Populate card with situation data"""
        self.title.setText(situation_data.get('situation_name', 'Unknown'))
        
        confidence = situation_data.get('confidence_score', 0)
        if confidence >= 80:
            color = '#4CAF50'  # Green
        elif confidence >= 50:
            color = '#FF9800'  # Orange
        else:
            color = '#F44336'  # Red
        
        self.confidence.setText(f"{confidence}%")
        self.confidence.setStyleSheet(f"color: {color};")
        
        self.description.setText(situation_data.get('situation_description', ''))
        
        severity = situation_data.get('severity', 'medium').upper()
        severity_map = {
            'HIGH': '⚠️ HIGH SEVERITY',
            'MEDIUM': '⚠️ MEDIUM',
            'LOW': '✓ LOW'
        }
        self.severity.setText(severity_map.get(severity, severity))

class LawWidget(QFrame):
    """
    Component for displaying a single law reference
    Shows: Law type, section, title, explanation
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-left: 4px solid #2196F3;
                padding: 8px;
                margin: 4px 0;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(4)
        
        # Header
        self.header = QLabel()
        self.header.setFont(QFont("Arial", 10, QFont.Bold))
        self.header.setStyleSheet("color: #2196F3;")
        self.layout.addWidget(self.header)
        
        # Title
        self.title = QLabel()
        self.title.setFont(QFont("Arial", 9, QFont.Bold))
        self.title.setStyleSheet("color: #ffffff;")
        self.layout.addWidget(self.title)
        
        # Explanation
        self.explanation = QLabel()
        self.explanation.setWordWrap(True)
        self.explanation.setStyleSheet("color: #cccccc; font-size: 10px;")
        self.layout.addWidget(self.explanation)
        
        # Key points
        self.key_points = QLabel()
        self.key_points.setWordWrap(True)
        self.key_points.setStyleSheet("color: #999999; font-size: 9px; margin-top: 4px;")
        self.layout.addWidget(self.key_points)
    
    def populate(self, law_data: dict):
        """Populate widget with law data"""
        self.header.setText(f"{law_data.get('type', 'Law')} — {law_data.get('section', '')}")
        self.title.setText(law_data.get('title', ''))
        self.explanation.setText(law_data.get('explanation', ''))
        
        points = law_data.get('key_points', [])
        if points:
            self.key_points.setText("• " + "\n• ".join(points[:3]))

class DisclaimerWidget(QFrame):
    """
    Disclaimer widget - displayed at the bottom of results
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border: 1px solid #FF9800;
                border-radius: 4px;
                padding: 10px;
                margin: 12px 0;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("⚠️ LEGAL DISCLAIMER")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet("color: #FF9800;")
        self.layout.addWidget(title)
        
        text = QLabel(
            "This tool provides general legal awareness and NOT legal advice.\n"
            "It explains laws in simple language for educational purposes.\n"
            "Always consult a qualified lawyer for specific legal situations.\n"
            "Police should be approached respectfully and lawfully."
        )
        text.setWordWrap(True)
        text.setStyleSheet("color: #cccccc; font-size: 10px; line-height: 1.4;")
        self.layout.addWidget(text)

class InputCard(QFrame):
    """
    Card component for user input
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #444444;
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(8)
