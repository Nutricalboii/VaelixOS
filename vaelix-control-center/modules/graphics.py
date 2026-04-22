"""
Graphics Module — GPU detection, refresh rate, compositor toggle.
"""
import subprocess
import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from core.ui_components import make_section, make_divider, VaelixButton, StatusBadge, CardFrame


class GpuDetectWorker(QThread):
    result = pyqtSignal(dict)

    def run(self):
        info = {"vendor": "Unknown", "model": "Unknown", "mode": "integrated"}
        try:
            lspci = subprocess.run(["lspci", "-mm"], capture_output=True, text=True, timeout=5)
            output = lspci.stdout.lower()
            if "nvidia" in output:
                info["vendor"] = "NVIDIA"
                info["mode"] = "hybrid" if "intel" in output or "amd" in output else "dedicated"
                # Get model
                for line in lspci.stdout.splitlines():
                    if "VGA" in line and "NVIDIA" in line.upper():
                        info["model"] = line.split('"')[-2] if '"' in line else line
                        break
            elif "amd" in output or "radeon" in output:
                info["vendor"] = "AMD"
                info["mode"] = "hybrid" if "intel" in output else "dedicated"
            elif "intel" in output:
                info["vendor"] = "Intel"
                info["mode"] = "integrated"
        except Exception:
            pass
        self.result.emit(info)


class GraphicsModule(QScrollArea):
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
        self._detect_gpu()

    def _build_ui(self):
        # GPU Info Card
        self.main_layout.addWidget(make_section(
            "GPU & Display",
            "Detected graphics hardware and display configuration."
        ))

        gpu_card = CardFrame()
        gpu_layout = QVBoxLayout(gpu_card)
        gpu_layout.setContentsMargins(20, 16, 20, 16)
        gpu_layout.setSpacing(10)

        info_row = QHBoxLayout()
        self.gpu_model_lbl = QLabel("Detecting GPU...")
        self.gpu_model_lbl.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.gpu_mode_badge = StatusBadge("Detecting", "#6b7280")

        info_row.addWidget(self.gpu_model_lbl)
        info_row.addStretch()
        info_row.addWidget(self.gpu_mode_badge)
        gpu_layout.addLayout(info_row)

        refresh_row = QHBoxLayout()
        refresh_lbl = QLabel("Refresh Rate Profile:")
        refresh_lbl.setFont(QFont("Inter", 10))

        self.refresh_combo = QComboBox()
        self.refresh_combo.addItems(["Auto (Max Available)", "60 Hz (Power Save)", "120 Hz", "144 Hz", "165 Hz", "240 Hz"])
        self.refresh_combo.setFixedHeight(36)
        self.refresh_combo.setStyleSheet("""
            QComboBox {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 0 12px;
                color: #cbd5e1;
            }
            QComboBox::drop-down { border: none; }
        """)

        refresh_apply = VaelixButton("Apply", "#3b82f6")
        refresh_apply.setFixedWidth(90)
        refresh_apply.clicked.connect(self._apply_refresh)

        refresh_row.addWidget(refresh_lbl)
        refresh_row.addWidget(self.refresh_combo, 1)
        refresh_row.addWidget(refresh_apply)
        gpu_layout.addLayout(refresh_row)
        self.main_layout.addWidget(gpu_card)

        self.main_layout.addWidget(make_divider())

        # Compositor
        self.main_layout.addWidget(make_section(
            "Compositor",
            "KWin compositor controls smooth windows and blur effects."
        ))

        compositor_card = CardFrame()
        comp_layout = QHBoxLayout(compositor_card)
        comp_layout.setContentsMargins(20, 16, 20, 16)
        comp_layout.setSpacing(16)

        self.compositor_badge = StatusBadge("ON", "#22c55e")
        comp_lbl = QLabel("KWin Compositor")
        comp_lbl.setFont(QFont("Inter", 11))

        toggle_comp = VaelixButton("Toggle On/Off", "#334155")
        toggle_comp.clicked.connect(self._toggle_compositor)

        game_comp = VaelixButton("Suspend for Game", "#ef4444")
        game_comp.clicked.connect(self._suspend_compositor)

        comp_layout.addWidget(comp_lbl)
        comp_layout.addStretch()
        comp_layout.addWidget(self.compositor_badge)
        comp_layout.addWidget(toggle_comp)
        comp_layout.addWidget(game_comp)
        self.main_layout.addWidget(compositor_card)

        self.main_layout.addStretch()

    def _detect_gpu(self):
        self.worker = GpuDetectWorker()
        self.worker.result.connect(self._on_gpu_detected)
        self.worker.start()

    def _on_gpu_detected(self, info: dict):
        model = info.get("model", "Unknown GPU")
        vendor = info.get("vendor", "Unknown")
        mode = info.get("mode", "integrated")

        self.gpu_model_lbl.setText(f"{vendor} — {model[:40]}")

        mode_colors = {
            "hybrid": "#f59e0b",
            "dedicated": "#3b82f6",
            "integrated": "#22c55e",
        }
        mode_labels = {
            "hybrid": "Hybrid Mode",
            "dedicated": "Dedicated GPU",
            "integrated": "Integrated",
        }
        self.gpu_mode_badge.set_status(
            mode_labels.get(mode, mode),
            mode_colors.get(mode, "#6b7280")
        )
        self.logger.log(f"GPU detected: {vendor} {model} [{mode}]")

    def _apply_refresh(self):
        self.logger.log(f"Refresh rate profile: {self.refresh_combo.currentText()}")
        # xrandr refresh rate switching would go here

    def _toggle_compositor(self):
        try:
            result = subprocess.run(
                ["qdbus", "org.kde.KWin", "/Compositor", "org.kde.kwin.Compositing.active"],
                capture_output=True, text=True, timeout=5
            )
            is_active = result.stdout.strip().lower() == "true"
            method = "suspend" if is_active else "resume"
            subprocess.run(["qdbus", "org.kde.KWin", "/Compositor", f"org.kde.kwin.Compositing.{method}"],
                           timeout=5)
            self.compositor_badge.set_status(
                "OFF" if is_active else "ON",
                "#ef4444" if is_active else "#22c55e"
            )
            self.logger.log(f"Compositor → {'suspended' if is_active else 'resumed'}")
        except Exception as e:
            self.logger.error(f"Compositor toggle failed: {e}")

    def _suspend_compositor(self):
        """Suspend compositor for maximum game FPS."""
        try:
            subprocess.run(["qdbus", "org.kde.KWin", "/Compositor",
                            "org.kde.kwin.Compositing.suspend"], timeout=5)
            self.compositor_badge.set_status("SUSPENDED", "#ef4444")
            self.logger.log("Compositor suspended for gaming")
        except Exception as e:
            self.logger.error(f"Compositor suspend failed: {e}")
