import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QCheckBox, 
                             QFrame, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon

class GlassCard(QFrame):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.setObjectName("GlassCard")
        self.setStyleSheet("""
            #GlassCard {
                background-color: rgba(30, 30, 45, 180);
                border: 1px solid rgba(120, 100, 255, 100);
                border-radius: 15px;
            }
            QLabel { color: white; background: transparent; }
        """)
        
        layout = QVBoxLayout(self)
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Outfit", 14, QFont.Weight.Bold))
        
        self.desc_label = QLabel(description)
        self.desc_label.setFont(QFont("Inter", 10))
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: rgba(255, 255, 255, 180);")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.desc_label)

class OnboardingWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Vaelix OS")
        self.setFixedSize(700, 500)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainWidget")
        self.central_widget.setStyleSheet("""
            #MainWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                stop:0 rgba(15, 15, 25, 255), stop:1 rgba(30, 30, 50, 255));
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 10);
            }
        """)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # Detect Hardware
        self.vhi = self._detect_hardware()
        
        self._init_welcome_screen()
        self._init_intelligence_screen()
        self._init_final_screen()
        
    def _detect_hardware(self):
        try:
            output = subprocess.check_output(["vaelix-hardware-detect"], text=True)
            data = {}
            for line in output.splitlines():
                k, v = line.split("=")
                data[k] = v
            return data
        except:
            return {"VHI_STORAGE": "Unknown", "VHI_RAM": "?", "VHI_GPU": "false", "VHI_PROFILE": "Standard"}

    def _init_welcome_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        logo = QLabel("✦")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 80px; color: #7864FF; margin-bottom: 20px;")
        
        title = QLabel("Welcome to Vaelix OS")
        title.setFont(QFont("Outfit", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white;")
        
        subtitle = QLabel("Titanium Velocity v1.1 — Stable Candidate")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 150);")
        
        btn = QPushButton("Initialize Intelligence")
        btn.setFixedSize(250, 50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #7864FF;
                color: white;
                border-radius: 25px;
                font-weight: bold;
                margin-top: 30px;
            }
            QPushButton:hover { background-color: #8C7AFF; }
        """)
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(btn, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.stack.addWidget(page)

    def _init_intelligence_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("System Intelligence")
        title.setFont(QFont("Outfit", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Hardware Info Grid
        info_layout = QHBoxLayout()
        info_layout.setSpacing(15)
        
        storage_card = GlassCard("Storage", f"{self.vhi['VHI_STORAGE']} Detected\nI/O scheduler tuned.")
        ram_card = GlassCard("Memory", f"{self.vhi['VHI_RAM']}GB Found\nPreload optimized.")
        gpu_status = "Discrete GPU found" if self.vhi['VHI_GPU'] == "true" else "Integrated Graphics"
        gpu_card = GlassCard("Graphics", f"{gpu_status}\nVelocity Mode ready.")
        
        info_layout.addWidget(storage_card)
        info_layout.addWidget(ram_card)
        info_layout.addWidget(gpu_card)
        layout.addLayout(info_layout)
        
        # Recommendation
        rec_box = QFrame()
        rec_box.setStyleSheet("background: rgba(120, 100, 255, 20); border-radius: 10px; border: 1px dashed #7864FF; margin-top: 20px;")
        rec_layout = QVBoxLayout(rec_box)
        
        profile = self.vhi['VHI_PROFILE']
        reason = ""
        if profile == "Lite":
            reason = "Reason: Rotational storage or lower RAM detected. Indexing reduced for smoothness."
        elif profile == "Velocity":
            reason = "Reason: High-end hardware found. Full visual effects enabled."
        else:
            reason = "Reason: Balanced workstation specs found."
            
        rec_title = QLabel(f"Recommended Profile: {profile}")
        rec_title.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        rec_title.setStyleSheet("color: #7864FF; border: none;")
        
        rec_desc = QLabel(reason)
        rec_desc.setStyleSheet("color: rgba(255, 255, 255, 180); border: none;")
        
        rec_layout.addWidget(rec_title)
        rec_layout.addWidget(rec_desc)
        layout.addWidget(rec_box)
        
        # Toggles
        self.snap_check = QCheckBox("Enable Resurrection (System Snapshots)")
        self.snap_check.setChecked(True)
        self.snap_check.setStyleSheet("color: white; margin-top: 10px;")
        layout.addWidget(self.snap_check)
        
        btn_layout = QHBoxLayout()
        skip_btn = QPushButton("Skip Setup")
        skip_btn.setStyleSheet("color: rgba(255, 255, 255, 100); background: transparent; font-weight: bold;")
        skip_btn.clicked.connect(self.close)
        
        apply_btn = QPushButton("Apply & Continue")
        apply_btn.setFixedSize(200, 40)
        apply_btn.setStyleSheet("background-color: #7864FF; color: white; border-radius: 20px; font-weight: bold;")
        apply_btn.clicked.connect(self._apply_and_finish)
        
        btn_layout.addWidget(skip_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(apply_btn)
        layout.addLayout(btn_layout)
        
        self.stack.addWidget(page)

    def _init_final_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        logo = QLabel("✓")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 80px; color: #00FF9D; margin-bottom: 20px;")
        
        title = QLabel("Initialization Complete")
        title.setFont(QFont("Outfit", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white;")
        
        desc = QLabel("Vaelix OS is now tuned to your hardware.\nHeadquarters is standing by.")
        desc.setFont(QFont("Inter", 11))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: rgba(255, 255, 255, 150);")
        
        btn = QPushButton("Enter Headquarters")
        btn.setFixedSize(250, 50)
        btn.setStyleSheet("background-color: #00FF9D; color: #0F0F19; border-radius: 25px; font-weight: bold; margin-top: 30px;")
        btn.clicked.connect(self.close)
        
        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()
        layout.addWidget(btn, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.stack.addWidget(page)

    def _apply_and_finish(self):
        profile = self.vhi['VHI_PROFILE']
        if profile == "Lite":
            subprocess.run(["vaelix-apply-lite"])
        
        if self.snap_check.isChecked():
            # Create first snapshot in background
            subprocess.Popen(["sudo", "timeshift", "--create", "--comments", "Initial Vaelix Setup"])
            
        # Mark as onboarded
        config_path = os.path.expanduser("~/.config/vaelix-onboarded")
        with open(config_path, "w") as f:
            f.write("done")
            
        self.stack.setCurrentIndex(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon.fromTheme("vaelix-logo"))
    
    wizard = OnboardingWizard()
    wizard.show()
    sys.exit(app.exec())
