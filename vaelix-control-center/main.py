import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize, QSettings
from PyQt6.QtGui import QIcon, QFont

# Internal imports
from core.theme_engine import THEMES, get_theme, get_qt_stylesheet
from core.logger import VaelixLogger

# Module imports
from modules.headquarters import HeadquartersModule
from modules.atmosphere import AtmosphereModule
from modules.performance import PerformanceModule
from modules.devtools import DevToolsModule
from modules.graphics import GraphicsModule
from modules.system import SystemModule

class VaelixControlCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = VaelixLogger()
        self.settings = QSettings("VaelixOS", "ControlCenter")
        
        self.setWindowTitle("Vaelix Control Center")
        self.setMinimumSize(900, 600)
        
        # Load geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(1050, 720)

        self.init_ui()
        self.apply_atmosphere("velocity") # Default starting point
        
    def init_ui(self):
        main_widget = QWidget()
        main_widget.setObjectName("centralWidget")
        self.setCentralWidget(main_widget)
        
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(12, 40, 12, 20)
        sidebar_layout.setSpacing(6)
        
        logo_lbl = QLabel("VAELIX")
        logo_lbl.setStyleSheet("font-size: 20px; font-weight: 900; margin-bottom: 30px; margin-left: 10px; letter-spacing: 2px;")
        sidebar_layout.addWidget(logo_lbl)

        self.stack = QStackedWidget()
        self.stack.setObjectName("contentStack")
        
        self.nav_buttons = {}
        menu_items = [
            ("Headquarters", "🏠", HeadquartersModule),
            ("Atmosphere", "🎨", AtmosphereModule),
            ("Performance", "⚡", PerformanceModule),
            ("Graphics", "🖼️", GraphicsModule),
            ("System", "🖥️", SystemModule),
            ("Dev Tools", "🛠️", DevToolsModule),
        ]
        
        for i, (name, icon, module_class) in enumerate(menu_items):
            # Instantiate module
            module = module_class(self.logger)
            self.stack.addWidget(module)
            
            # Sidebar button
            btn = QPushButton(f"{icon}  {name}")
            btn.setCheckable(True)
            btn.setProperty("active", "false")
            btn.setFixedHeight(45)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, idx=i: self.switch_page(idx))
            
            sidebar_layout.addWidget(btn)
            self.nav_buttons[i] = btn
            
        sidebar_layout.addStretch()
        
        version_lbl = QLabel("v2.1 Quantum Edge")
        version_lbl.setStyleSheet("color: rgba(255,255,255,0.2); font-size: 10px; margin-left: 10px;")
        sidebar_layout.addWidget(version_lbl)
        
        # --- Content Area ---
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.stack)
        
        layout.addWidget(self.sidebar)
        layout.addWidget(content_container)

        # Start on Atmosphere page
        self.switch_page(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in self.nav_buttons.items():
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def apply_atmosphere(self, theme_id):
        theme = get_theme(theme_id)
        self.setStyleSheet(get_qt_stylesheet(theme))
        self.logger.log(f"UI Atmosphere updated: {theme.name}")

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Global font setup
    font = QFont("Inter", 10)
    app.setFont(font)
    
    window = VaelixControlCenter()
    window.show()
    sys.exit(app.exec())
