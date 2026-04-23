"""
Dev Tools Module — One-click install for Docker, Git stack, Node, Python, Android.
"""
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from core.ui_components import make_section, make_divider, VaelixButton, StatusBadge, CardFrame


class InstallWorker(QThread):
    output = pyqtSignal(str)
    done = pyqtSignal(bool)

    def __init__(self, packages: list[str]):
        super().__init__()
        self.packages = packages

    def run(self):
        self.output.emit(f"Installing: {', '.join(self.packages)}...\n")
        try:
            proc = subprocess.Popen(
                ["pkexec", "apt", "install", "-y"] + self.packages,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            for line in proc.stdout:
                self.output.emit(line)
            proc.wait()
            self.done.emit(proc.returncode == 0)
        except Exception as e:
            self.output.emit(f"Error: {e}\n")
            self.done.emit(False)


class DevToolsModule(QScrollArea):
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

    def _build_ui(self):
        self.main_layout.addWidget(make_section(
            "Developer Stack",
            "One-click install curated dev tools. All installs are logged."
        ))

        stacks = [
            {
                "icon": "🐳",
                "name": "Docker & Compose",
                "desc": "Container runtime for development and deployment",
                "packages": ["docker.io", "docker-compose"],
                "color": "#3b82f6",
            },
            {
                "icon": "🐙",
                "name": "Git Stack",
                "desc": "Git, GitHub CLI, SSH key tools",
                "packages": ["git", "gh", "git-lfs", "openssh-client"],
                "color": "#f59e0b",
            },
            {
                "icon": "🟢",
                "name": "Node.js (LTS)",
                "desc": "Node + npm + nvm for web development",
                "packages": ["nodejs", "npm"],
                "color": "#22c55e",
            },
            {
                "icon": "🐍",
                "name": "Python Stack",
                "desc": "Python 3, pip, venv, and dev essentials",
                "packages": ["python3", "python3-pip", "python3-venv", "python3-dev"],
                "color": "#a855f7",
            },
            {
                "icon": "📱",
                "name": "Android Tools",
                "desc": "ADB, Fastboot, scrcpy for device debugging",
                "packages": ["adb", "fastboot", "scrcpy"],
                "color": "#ef4444",
            },
            {
                "icon": "🦀",
                "name": "Rust Toolchain",
                "desc": "rustup, cargo, rust analyzer",
                "packages": ["rustc", "cargo"],
                "color": "#f97316",
            },
        ]

        for stack in stacks:
            card = CardFrame()
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(20, 14, 20, 14)
            card_layout.setSpacing(16)

            icon_lbl = QLabel(stack["icon"])
            icon_lbl.setFont(QFont("Noto Color Emoji", 20))
            icon_lbl.setFixedWidth(40)

            text_col = QVBoxLayout()
            text_col.setSpacing(2)
            name_lbl = QLabel(stack["name"])
            name_lbl.setFont(QFont("Inter", 11, QFont.Weight.Bold))
            desc_lbl = QLabel(stack["desc"])
            desc_lbl.setFont(QFont("Inter", 9))
            desc_lbl.setStyleSheet("color: #475569;")
            text_col.addWidget(name_lbl)
            text_col.addWidget(desc_lbl)

            install_btn = VaelixButton("Install", stack["color"])
            install_btn.setFixedWidth(100)
            install_btn.clicked.connect(
                lambda _, p=stack["packages"], n=stack["name"]: self._install_stack(p, n)
            )
            self.status_badge = StatusBadge("Ready", "#6b7280")

            card_layout.addWidget(icon_lbl)
            card_layout.addLayout(text_col, 1)
            card_layout.addWidget(install_btn)

            self.main_layout.addWidget(card)

        self.main_layout.addWidget(make_divider())

        # Terminal output
        self.main_layout.addWidget(make_section("Install Output", "Live install progress log."))

        log_card = CardFrame()
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(16, 12, 16, 12)

        self.term_output = QTextEdit()
        self.term_output.setReadOnly(True)
        self.term_output.setFixedHeight(160)
        self.term_output.setFont(QFont("monospace", 9))
        self.term_output.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.5);
                color: #22c55e;
                border: none;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        self.term_output.setPlaceholderText("Install output will appear here...")

        log_layout.addWidget(self.term_output)
        self.main_layout.addWidget(log_card)
        self.main_layout.addStretch()

    def _install_stack(self, packages: list[str], name: str):
        self.term_output.clear()
        self.term_output.append(f"▶ Starting install: {name}\n")
        self.logger.log(f"Dev stack install started: {name}")

        self.worker = InstallWorker(packages)
        self.worker.output.connect(self.term_output.append)
        self.worker.done.connect(
            lambda ok: self.term_output.append(
                f"\n{'✅ Install complete!' if ok else '❌ Install failed.'}"
            )
        )
        self.worker.start()
