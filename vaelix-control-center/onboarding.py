import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QCheckBox, 
                             QFrame, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon

# Import themes for atmosphere picker
# (In real deployment, we'd import core.theme_engine)
THEMES = {
    "velocity": "Titanium Velocity",
    "amethyst": "Amethyst Noir",
    "noir": "Executive Noir",
    "arctic": "Arctic Glass",
    "quantum": "Quantum Edge"
}

class OnboardingWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vaelix OS 2.0 — Renaissance Setup")
        self.setFixedSize(800, 550)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainWidget")
        self.central_widget.setStyleSheet("""
            #MainWidget {
                background-color: #080810;
                border-radius: 20px;
                border: 1px solid rgba(139, 92, 246, 0.3);
            }
            QLabel { color: #e2e8f0; }
            QPushButton {
                background: #8b5cf6;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover { background: #a78bfa; }
        """)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        self._init_screens()
        
    def _init_screens(self):
        self._init_welcome()
        self._init_atmosphere()
        self._init_vhi()
        self._init_final()
        
    def _init_welcome(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo = QLabel("✦")
        logo.setStyleSheet("font-size: 80px; color: #8b5cf6; margin-bottom: 20px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Welcome to Renaissance")
        title.setFont(QFont("Syne", 32, QFont.Weight.Bold))
        
        subtitle = QLabel("The next evolution of Vaelix OS. Let's configure your identity.")
        subtitle.setStyleSheet("color: #94a3b8; font-size: 14px; margin-bottom: 30px;")
        
        btn = QPushButton("Begin Initiation")
        btn.setFixedSize(200, 50)
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        layout.addWidget(logo)
        layout.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn, 0, Qt.AlignmentFlag.AlignCenter)
        self.stack.addWidget(page)

    def _init_atmosphere(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Choose Your Atmosphere")
        title.setFont(QFont("Syne", 20, QFont.Weight.Bold))
        
        grid_layout = QHBoxLayout()
        for tid, name in THEMES.items():
            btn = QPushButton(name)
            btn.setFixedHeight(100)
            btn.setStyleSheet(f"background: #13131f; border: 1px solid rgba(139,92,246,0.2);")
            grid_layout.addWidget(btn)
            
        layout.addWidget(title)
        layout.addLayout(grid_layout)
        
        next_btn = QPushButton("Apply & Continue")
        next_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        layout.addWidget(next_btn, 0, Qt.AlignmentFlag.AlignRight)
        self.stack.addWidget(page)

    def _init_vhi(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Hardware Intelligence (VHI 2.0)")
        title.setFont(QFont("Syne", 20, QFont.Weight.Bold))
        
        report = QLabel("Detecting hardware profiles...\n\nCPU: Optimized\nGPU: Adaptive\nRAM: Performance Tier 1\n\nVaelix has chosen the 'Velocity' profile for your system.")
        report.setStyleSheet("background: #0e0e1a; padding: 20px; border-radius: 10px; color: #22d3ee; font-family: 'Space Mono';")
        
        layout.addWidget(title)
        layout.addWidget(report)
        
        next_btn = QPushButton("Confirm Hardware Profile")
        next_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        layout.addWidget(next_btn, 0, Qt.AlignmentFlag.AlignRight)
        self.stack.addWidget(page)

    def _init_final(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Final Hardening")
        title.setFont(QFont("Syne", 20, QFont.Weight.Bold))
        
        h_box = QVBoxLayout()
        h_box.addWidget(QCheckBox("Enable Graphene-grade Security Hardening"))
        h_box.addWidget(QCheckBox("Enable Developer/Rust Tooling Stack"))
        h_box.addWidget(QCheckBox("Log Anonymous Usage Statistics (No Personal Data)"))
        
        layout.addWidget(title)
        layout.addLayout(h_box)
        
        finish_btn = QPushButton("Complete Renaissance")
        finish_btn.clicked.connect(self.close)
        layout.addWidget(finish_btn, 0, Qt.AlignmentFlag.AlignCenter)
        self.stack.addWidget(page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OnboardingWizard()
    window.show()
    sys.exit(app.exec())
