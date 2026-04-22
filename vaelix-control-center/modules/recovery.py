"""
Recovery Module — Logs viewer, safe mode, rollback helper.
"""
import subprocess
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.ui_components import make_section, make_divider, VaelixButton, CardFrame, StatusBadge


class RecoveryModule(QScrollArea):
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
        # Warning banner
        warn_card = CardFrame()
        warn_card.setStyleSheet("""
            QFrame {
                background: rgba(239, 68, 68, 0.08);
                border: 1px solid rgba(239, 68, 68, 0.2);
                border-radius: 12px;
            }
        """)
        warn_layout = QHBoxLayout(warn_card)
        warn_layout.setContentsMargins(16, 12, 16, 12)
        warn_lbl = QLabel("⚠️  Recovery tools are for advanced users. All actions are logged and reversible where possible.")
        warn_lbl.setFont(QFont("Inter", 9))
        warn_lbl.setStyleSheet("color: #fca5a5; background: transparent; border: none;")
        warn_lbl.setWordWrap(True)
        warn_layout.addWidget(warn_lbl)
        self.main_layout.addWidget(warn_card)

        # Log viewer
        self.main_layout.addWidget(make_section("System Logs", "Recent journal entries for diagnostics."))

        log_card = CardFrame()
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(16, 12, 16, 12)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFixedHeight(200)
        self.log_display.setFont(QFont("JetBrains Mono", 9))
        self.log_display.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.4);
                color: #94a3b8;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-family: monospace;
            }
        """)
        self.log_display.setPlaceholderText("Press 'Load Logs' to fetch journal entries...")

        log_btns = QHBoxLayout()
        load_btn = VaelixButton("Load Journal", "#3b82f6")
        load_btn.clicked.connect(self._load_journal)
        vcc_btn = VaelixButton("VCC Activity Log", "#6b7280")
        vcc_btn.clicked.connect(self._load_vcc_log)
        log_btns.addWidget(load_btn)
        log_btns.addWidget(vcc_btn)
        log_btns.addStretch()

        log_layout.addWidget(self.log_display)
        log_layout.addLayout(log_btns)
        self.main_layout.addWidget(log_card)

        self.main_layout.addWidget(make_divider())

        # Rollback & Safe Mode
        self.main_layout.addWidget(make_section("System Recovery", "Kernel and system rollback utilities."))

        recovery_card = CardFrame()
        rec_layout = QVBoxLayout(recovery_card)
        rec_layout.setContentsMargins(20, 16, 20, 16)
        rec_layout.setSpacing(12)

        actions = [
            ("🔄 Reboot to Previous Kernel", "#f59e0b", self._reboot_prev_kernel),
            ("🛡️  Boot to Recovery Mode", "#ef4444", self._boot_recovery),
            ("📸 Launch Timeshift Snapshot", "#22c55e", self._launch_timeshift),
            ("🔧 Re-apply Vaelix Defaults", "#3b82f6", self._reapply_defaults),
        ]
        for label, color, func in actions:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setFont(QFont("Inter", 10))
            btn = VaelixButton("Run", color)
            btn.setFixedWidth(90)
            btn.clicked.connect(func)
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(btn)
            rec_layout.addLayout(row)

        self.main_layout.addWidget(recovery_card)
        self.main_layout.addStretch()

    def _load_journal(self):
        try:
            result = subprocess.run(
                ["journalctl", "-n", "80", "--no-pager", "-p", "err..warning"],
                capture_output=True, text=True, timeout=10
            )
            self.log_display.setPlainText(result.stdout or "No recent errors found.")
        except Exception as e:
            self.log_display.setPlainText(f"Failed to load journal: {e}")
        self.logger.log("Journal loaded")

    def _load_vcc_log(self):
        log_path = os.path.expanduser(
            f"~/.local/share/vaelix-control-center/logs"
        )
        try:
            import glob
            logs = sorted(glob.glob(f"{log_path}/*.log"), reverse=True)
            if logs:
                with open(logs[0]) as f:
                    self.log_display.setPlainText(f.read())
            else:
                self.log_display.setPlainText("No VCC logs found yet.")
        except Exception as e:
            self.log_display.setPlainText(f"Log read error: {e}")

    def _reboot_prev_kernel(self):
        subprocess.Popen(["pkexec", "grub-reboot", "1,0"])
        subprocess.Popen(["pkexec", "reboot"])
        self.logger.log("Rebooting to previous kernel")

    def _boot_recovery(self):
        subprocess.Popen(["pkexec", "systemctl", "reboot", "--boot-loader-entry=auto-reboot-to-firmware-setup"])
        self.logger.log("Recovery mode boot requested")

    def _launch_timeshift(self):
        subprocess.Popen(["pkexec", "timeshift-gtk"])
        self.logger.log("Timeshift launched")

    def _reapply_defaults(self):
        subprocess.Popen(["lookandfeeltool", "-a", "com.github.vinceliuice.WhiteSur-dark"])
        self.logger.log("Vaelix defaults re-applied")
