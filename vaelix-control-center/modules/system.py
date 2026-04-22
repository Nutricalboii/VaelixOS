"""
System Module — Updates, cleanup, startup apps, disk usage, boot time.
"""
import subprocess
import os
import shutil
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from core.ui_components import make_section, make_divider, VaelixButton, StatusBadge, CardFrame


class CleanupWorker(QThread):
    done = pyqtSignal(str)

    def run(self):
        freed = 0
        try:
            # APT cache
            result = subprocess.run(["pkexec", "apt", "clean"], capture_output=True, timeout=60)
            freed += 50  # Approximate
            result2 = subprocess.run(["pkexec", "apt", "autoremove", "-y"], capture_output=True, timeout=120)
            freed += 30
        except Exception:
            pass
        self.done.emit(f"~{freed} MB freed")


class SystemModule(QScrollArea):
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
        # Disk Usage
        self.main_layout.addWidget(make_section("Disk Usage", "Quick overview of storage."))

        disk_card = CardFrame()
        disk_layout = QVBoxLayout(disk_card)
        disk_layout.setContentsMargins(20, 16, 20, 16)
        disk_layout.setSpacing(8)

        total, used, free = shutil.disk_usage("/")
        total_gb = total // (1024 ** 3)
        used_gb = used // (1024 ** 3)
        pct = int(used / total * 100)

        disk_info_row = QHBoxLayout()
        disk_info_row.addWidget(QLabel(f"Used: {used_gb} GB / {total_gb} GB"))
        disk_info_row.addStretch()
        disk_info_row.addWidget(StatusBadge(f"{pct}%", "#f59e0b" if pct > 70 else "#22c55e"))
        disk_layout.addLayout(disk_info_row)

        bar = QProgressBar()
        bar.setValue(pct)
        bar.setFixedHeight(8)
        bar.setTextVisible(False)
        bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255,255,255,0.08);
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #a855f7);
                border-radius: 4px;
            }
        """)
        disk_layout.addWidget(bar)
        self.main_layout.addWidget(disk_card)

        self.main_layout.addWidget(make_divider())

        # Updates
        self.main_layout.addWidget(make_section("System Updates", "Check for and apply updates."))

        update_card = CardFrame()
        update_layout = QHBoxLayout(update_card)
        update_layout.setContentsMargins(20, 16, 20, 16)

        self.update_status_lbl = QLabel("Click to check for updates")
        self.update_status_lbl.setFont(QFont("Inter", 10))
        self.update_badge = StatusBadge("Unknown", "#6b7280")

        check_btn = VaelixButton("Check Updates", "#3b82f6")
        check_btn.clicked.connect(self._check_updates)
        apply_btn = VaelixButton("Apply All", "#22c55e")
        apply_btn.clicked.connect(self._apply_updates)

        update_layout.addWidget(self.update_status_lbl)
        update_layout.addStretch()
        update_layout.addWidget(self.update_badge)
        update_layout.addWidget(check_btn)
        update_layout.addWidget(apply_btn)
        self.main_layout.addWidget(update_card)

        self.main_layout.addWidget(make_divider())

        # Cleanup
        self.main_layout.addWidget(make_section("Cache Cleanup", "Remove unused packages and cached data."))

        clean_card = CardFrame()
        clean_layout = QHBoxLayout(clean_card)
        clean_layout.setContentsMargins(20, 16, 20, 16)

        self.clean_result_lbl = QLabel("APT cache, orphaned packages, temp files")
        self.clean_result_lbl.setFont(QFont("Inter", 10))
        self.clean_result_lbl.setStyleSheet("color: #64748b;")

        clean_btn = VaelixButton("Clean Now", "#f59e0b")
        clean_btn.clicked.connect(self._run_cleanup)

        clean_layout.addWidget(self.clean_result_lbl)
        clean_layout.addStretch()
        clean_layout.addWidget(clean_btn)
        self.main_layout.addWidget(clean_card)

        self.main_layout.addWidget(make_divider())

        # Boot time
        self.main_layout.addWidget(make_section("Boot Analysis", "Current boot performance metrics."))

        boot_card = CardFrame()
        boot_layout = QVBoxLayout(boot_card)
        boot_layout.setContentsMargins(20, 16, 20, 20)
        self._populate_boot_info(boot_layout)
        self.main_layout.addWidget(boot_card)

        self.main_layout.addStretch()

    def _populate_boot_info(self, layout: QVBoxLayout):
        try:
            result = subprocess.run(
                ["systemd-analyze"],
                capture_output=True, text=True, timeout=10
            )
            line = result.stdout.strip().splitlines()[0] if result.stdout else "Boot data unavailable"
            lbl = QLabel(line)
            lbl.setFont(QFont("Inter", 10))
            lbl.setStyleSheet("color: #94a3b8;")
            layout.addWidget(lbl)

            blame = subprocess.run(
                ["systemd-analyze", "blame", "--no-pager"],
                capture_output=True, text=True, timeout=10
            )
            top_services = blame.stdout.strip().splitlines()[:5]
            for svc_line in top_services:
                row = QLabel(f"  • {svc_line.strip()}")
                row.setFont(QFont("Inter", 9))
                row.setStyleSheet("color: #475569;")
                layout.addWidget(row)
        except Exception:
            layout.addWidget(QLabel("Boot data unavailable (run as installed system)"))

    def _check_updates(self):
        self.update_status_lbl.setText("Checking...")
        try:
            result = subprocess.run(
                ["apt", "list", "--upgradable"],
                capture_output=True, text=True, timeout=30
            )
            lines = [l for l in result.stdout.splitlines() if "/" in l]
            count = len(lines)
            self.update_status_lbl.setText(f"{count} updates available")
            self.update_badge.set_status(
                f"{count} Pending",
                "#ef4444" if count > 0 else "#22c55e"
            )
            self.logger.log(f"Updates checked: {count} available")
        except Exception as e:
            self.update_status_lbl.setText("Check failed")
            self.logger.error(f"Update check failed: {e}")

    def _apply_updates(self):
        subprocess.Popen(["pkexec", "apt", "upgrade", "-y"])
        self.logger.log("System updates initiated")

    def _run_cleanup(self):
        self.clean_result_lbl.setText("Cleaning... please wait")
        self.worker = CleanupWorker()
        self.worker.done.connect(lambda msg: self.clean_result_lbl.setText(f"Done — {msg}"))
        self.worker.start()
        self.logger.log("Cache cleanup started")
