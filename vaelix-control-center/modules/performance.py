"""
Performance Module — CPU governors, service tuning, battery/gaming modes.
"""
import subprocess
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QButtonGroup,
    QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from core.ui_components import (
    make_section, make_divider, VaelixButton, StatusBadge, CardFrame
)


class CpuWorker(QThread):
    done = pyqtSignal(bool)

    def __init__(self, governor: str):
        super().__init__()
        self.governor = governor

    def run(self):
        cores = os.cpu_count() or 1
        success = True
        for i in range(cores):
            path = f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor"
            try:
                result = subprocess.run(
                    ["pkexec", "bash", "-c", f"echo {self.governor} > {path}"],
                    capture_output=True, timeout=10
                )
                if result.returncode != 0:
                    success = False
            except Exception:
                success = False
        self.done.emit(success)


class ModeButton(QPushButton):
    def __init__(self, icon: str, label: str, desc: str, color: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self._color = color
        self._label = label
        self._icon = icon
        self.setFont(QFont("Inter", 10))
        self._update_style(False)

    def _update_style(self, active: bool):
        if active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {self._color}22;
                    border: 2px solid {self._color};
                    border-radius: 14px;
                    padding: 10px;
                    text-align: left;
                    color: #f1f5f9;
                    font-weight: 700;
                }}
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(17, 25, 45, 0.7);
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 14px;
                    padding: 10px;
                    text-align: left;
                    color: #94a3b8;
                }
                QPushButton:hover {
                    background: rgba(30, 41, 59, 0.9);
                    border: 1px solid rgba(255,255,255,0.14);
                    color: #e2e8f0;
                }
            """)

    def setActive(self, active: bool):
        self._update_style(active)


class PerformanceModule(QScrollArea):
    def __init__(self, logger, parent=None):
        super().__init__(parent)
        self.logger = logger
        self.setWidgetResizable(True)
        self.setStyleSheet("background: transparent; border: none;")

        content = QWidget()
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        self.main_layout.setSpacing(28)

        self._build_ui()
        self.setWidget(content)

    def _build_ui(self):
        # Status row
        status_row = QHBoxLayout()
        self.governor_badge = StatusBadge("Detecting...", "#94a3b8")
        self._detect_current_governor()
        status_row.addWidget(QLabel("Current Profile:"))
        status_row.addWidget(self.governor_badge)
        status_row.addStretch()
        self.main_layout.addLayout(status_row)

        self.main_layout.addWidget(make_section(
            "Performance Profile",
            "Choose how Vaelix OS manages your CPU and system resources."
        ))

        # Mode selection card
        modes_card = CardFrame()
        modes_layout = QHBoxLayout(modes_card)
        modes_layout.setContentsMargins(20, 20, 20, 20)
        modes_layout.setSpacing(16)

        self.mode_buttons = []
        self.mode_group = QButtonGroup()
        self.mode_group.setExclusive(True)

        modes = [
            ("🔋", "Battery Saver", "Minimal power draw", "#22c55e", "powersave"),
            ("⚖️", "Balanced", "Smart power/perf mix", "#3b82f6", "schedutil"),
            ("🚀", "Performance", "Max CPU clock speed", "#f59e0b", "performance"),
            ("🎮", "Gaming Mode", "Performance + GPU boost", "#ef4444", "performance"),
        ]

        for i, (icon, label, desc, color, gov) in enumerate(modes):
            btn = ModeButton(icon, label, desc, color)
            btn.setText(f"{icon}  {label}\n\n{desc}")
            btn.clicked.connect(lambda _, g=gov, b=btn: self._apply_governor(g, b))
            self.mode_group.addButton(btn, i)
            self.mode_buttons.append((btn, gov))
            modes_layout.addWidget(btn)

        modes_layout.addStretch()
        self.main_layout.addWidget(modes_card)

        self.main_layout.addWidget(make_divider())

        # Services section
        self.main_layout.addWidget(make_section(
            "Background Services",
            "Disable unused services to free up RAM and reduce boot time."
        ))

        services_card = CardFrame()
        services_layout = QVBoxLayout(services_card)
        services_layout.setContentsMargins(20, 16, 20, 16)

        services = [
            ("🖨️ CUPS Print Spooler", "cups", False),
            ("🔵 Bluetooth", "bluetooth", True),
            ("📍 Location Services", "geoclue", False),
        ]

        for name, svc, default_on in services:
            row = QHBoxLayout()
            lbl = QLabel(name)
            lbl.setFont(QFont("Inter", 10))
            badge = StatusBadge("ON" if default_on else "OFF",
                                "#22c55e" if default_on else "#ef4444")

            toggle_btn = VaelixButton("Toggle", "#334155")
            toggle_btn.setFixedWidth(90)
            toggle_btn.clicked.connect(lambda _, s=svc, b=badge: self._toggle_service(s, b))

            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(badge)
            row.addWidget(toggle_btn)
            services_layout.addLayout(row)

        self.main_layout.addWidget(services_card)
        self.main_layout.addStretch()

    def _detect_current_governor(self):
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor") as f:
                gov = f.read().strip()
                colors = {"powersave": "#22c55e", "schedutil": "#3b82f6", "performance": "#ef4444"}
                self.governor_badge.set_status(gov.capitalize(), colors.get(gov, "#94a3b8"))
        except Exception:
            self.governor_badge.set_status("Unknown", "#64748b")

    def _apply_governor(self, governor: str, active_btn: ModeButton):
        for btn, _ in self.mode_buttons:
            btn.setActive(False)
        active_btn.setActive(True)

        self.worker = CpuWorker(governor)
        self.worker.done.connect(lambda ok: self._on_governor_done(ok, governor))
        self.worker.start()
        self.logger.log(f"Applying CPU governor: {governor}")

    def _on_governor_done(self, success: bool, governor: str):
        if success:
            self._detect_current_governor()
        self.logger.log(f"Governor switch to '{governor}': {'OK' if success else 'FAILED'}")

    def _toggle_service(self, service: str, badge: StatusBadge):
        # Check current status and toggle
        try:
            result = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
            is_active = result.stdout.strip() == "active"
            action = "stop" if is_active else "start"
            subprocess.run(["pkexec", "systemctl", action, service], capture_output=True, timeout=10)
            badge.set_status("OFF" if is_active else "ON",
                             "#ef4444" if is_active else "#22c55e")
            self.logger.log(f"Service {service} → {action}")
        except Exception as e:
            self.logger.error(f"Toggle service {service} failed: {e}")
