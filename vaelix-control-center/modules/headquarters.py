import psutil
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from core.ui_components import (
    make_section, make_divider, VaelixButton, StatusBadge, CardFrame, StatCard
)

class StatsWorker(QThread):
    stats_updated = pyqtSignal(dict)

    def run(self):
        while True:
            try:
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                
                temp = "N/A"
                try:
                    temps = psutil.sensors_temperatures()
                    if 'coretemp' in temps:
                        temp = f"{int(temps['coretemp'][0].current)}°C"
                    elif 'cpu_thermal' in temps:
                        temp = f"{int(temps['cpu_thermal'][0].current)}°C"
                except:
                    pass

                self.stats_updated.emit({
                    'cpu': f"{cpu}%",
                    'ram': f"{ram}%",
                    'temp': temp,
                    'disk': f"{disk}%"
                })
            except Exception:
                pass
            self.msleep(2000)

class HeadquartersModule(QScrollArea):
    def __init__(self, logger, parent=None):
        super().__init__(parent)
        self.logger = logger
        self.setWidgetResizable(True)
        self.setStyleSheet("background: transparent; border: none;")
        self.viewport().setStyleSheet("background: transparent; border: none;")

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        self.main_layout.setSpacing(28)

        self._build_ui()
        self.setWidget(content)
        
        # Stats Thread
        self.worker = StatsWorker()
        self.worker.stats_updated.connect(self._on_stats_updated)
        self.worker.start()

    def _build_ui(self):
        # 1. Live Stats Grid
        self.main_layout.addWidget(make_section("Headquarters: Titanium Velocity", "Real-time system intelligence."))
        
        stats_grid = QGridLayout()
        stats_grid.setSpacing(16)
        
        self.cpu_card = StatCard("⚡", "CPU Load", "--", "#ef4444")
        self.ram_card = StatCard("🧠", "RAM Usage", "--", "#3b82f6")
        self.temp_card = StatCard("🔥", "Thermal", "--", "#f59e0b")
        self.disk_card = StatCard("💾", "Storage", "--", "#10b981")
        
        stats_grid.addWidget(self.cpu_card, 0, 0)
        stats_grid.addWidget(self.ram_card, 0, 1)
        stats_grid.addWidget(self.temp_card, 0, 2)
        stats_grid.addWidget(self.disk_card, 0, 3)
        
        self.main_layout.addLayout(stats_grid)
        self.main_layout.addWidget(make_divider())

        # 2. Performance Modes (Gaming Mode)
        self.main_layout.addWidget(make_section("Intelligence Toggles", "One-click system optimization."))
        
        toggles_card = CardFrame()
        toggles_layout = QVBoxLayout(toggles_card)
        toggles_layout.setContentsMargins(20, 20, 20, 20)
        toggles_layout.setSpacing(16)
        
        # Gaming Mode Row
        gaming_row = QHBoxLayout()
        gaming_info = QVBoxLayout()
        gaming_title = QLabel("Gaming Beast Mode")
        gaming_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        gaming_desc = QLabel("Max performance governor, disable animations, GPU priority.")
        gaming_desc.setStyleSheet("color: #64748b; font-size: 11px;")
        gaming_info.addWidget(gaming_title)
        gaming_info.addWidget(gaming_desc)
        
        self.gaming_btn = VaelixButton("Engage", "#ef4444")
        self.gaming_btn.setFixedWidth(120)
        self.gaming_btn.clicked.connect(self._toggle_gaming_mode)
        
        gaming_row.addLayout(gaming_info)
        gaming_row.addStretch()
        gaming_row.addWidget(self.gaming_btn)
        toggles_layout.addLayout(gaming_row)
        
        self.main_layout.addWidget(toggles_card)
        self.main_layout.addStretch()

    def _on_stats_updated(self, data):
        self.cpu_card.update_value(data['cpu'])
        self.ram_card.update_value(data['ram'])
        self.temp_card.update_value(data['temp'])
        self.disk_card.update_value(data['disk'])

    def _toggle_gaming_mode(self):
        is_active = self.gaming_btn.text() == "Disengage"
        if not is_active:
            subprocess.run(["vx", "game", "on"])
            self.gaming_btn.setText("Disengage")
            self.gaming_btn.setStyleSheet("background: #475569; color: white; border-radius: 10px;")
            self.logger.log("Gaming Mode: ENGAGED")
        else:
            subprocess.run(["vx", "game", "off"])
            self.gaming_btn.setText("Engage")
            self.gaming_btn.setStyleSheet("background: #ef4444; color: white; border-radius: 10px;")
            self.logger.log("Gaming Mode: DISENGAGED")
