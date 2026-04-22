"""
Vaelix Atmosphere Switcher Module
One-click theme switching with live preview cards for all 5 identities.
"""
import json
import os
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QGridLayout, QPushButton
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

from core.ui_components import make_section, make_divider, VaelixButton, CardFrame
from core.theme_engine import THEMES, VaelixTheme, get_qt_stylesheet

PREFS_PATH = os.path.expanduser("~/.config/vaelix/theme.json")


def save_theme_pref(theme_id: str):
    os.makedirs(os.path.dirname(PREFS_PATH), exist_ok=True)
    with open(PREFS_PATH, "w") as f:
        json.dump({"active": theme_id}, f)


def load_theme_pref() -> str:
    try:
        with open(PREFS_PATH) as f:
            return json.load(f).get("active", "velocity")
    except Exception:
        return "velocity"


class ThemeCard(QFrame):
    """Premium atmosphere identity card with live swatch and selector."""

    selected = pyqtSignal(str)  # emits theme_id

    def __init__(self, theme: VaelixTheme, is_active: bool = False, parent=None):
        super().__init__(parent)
        self.theme = theme
        self._active = is_active
        self.setFixedSize(210, 180)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._build()
        self._apply_style()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Color preview strip
        preview = QFrame()
        preview.setFixedHeight(80)
        preview.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 {self.theme.base_void},
                    stop:0.6 {self.theme.base_panel},
                    stop:1 {self.theme.base_border});
                border-top-left-radius: 14px;
                border-top-right-radius: 14px;
            }}
        """)

        # Accent swatch dots
        dots_layout = QHBoxLayout(preview)
        dots_layout.setContentsMargins(12, 0, 12, 8)
        dots_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        for color, size in [
            (self.theme.base_panel, 10),
            (self.theme.base_border, 10),
            (self.theme.accent, 12),
        ]:
            dot = QFrame()
            dot.setFixedSize(size, size)
            dot.setStyleSheet(f"""
                QFrame {{
                    background: {color};
                    border-radius: {size // 2}px;
                    border: 1px solid rgba(255,255,255,0.08);
                }}
            """)
            dots_layout.addWidget(dot)
        dots_layout.addStretch()

        # Info panel
        info = QFrame()
        info.setStyleSheet(f"background: {self.theme.base_primary}; border-bottom-left-radius: 14px; border-bottom-right-radius: 14px;")
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(14, 10, 14, 12)
        info_layout.setSpacing(2)

        name_lbl = QLabel(self.theme.name)
        name_lbl.setFont(QFont("Space Grotesk", 10, QFont.Weight.Bold))
        name_lbl.setStyleSheet(f"color: {self.theme.text_primary}; background: transparent;")

        tag_lbl = QLabel(self.theme.tagline)
        tag_lbl.setFont(QFont("Inter", 8))
        tag_lbl.setStyleSheet(f"color: {self.theme.text_muted}; background: transparent;")
        tag_lbl.setWordWrap(True)

        info_layout.addWidget(name_lbl)
        info_layout.addWidget(tag_lbl)

        layout.addWidget(preview)
        layout.addWidget(info)

    def _apply_style(self):
        border_col = self.theme.accent if self._active else "rgba(255,255,255,0.07)"
        self.setStyleSheet(f"""
            QFrame {{
                border: {'2' if self._active else '1'}px solid {border_col};
                border-radius: 14px;
            }}
        """)

    def setActive(self, active: bool):
        self._active = active
        self._apply_style()

    def mousePressEvent(self, event):
        self.selected.emit(self.theme.id)
        super().mousePressEvent(event)


class AutoScheduler(QThread):
    """Auto-switch themes based on time of day."""
    theme_suggested = pyqtSignal(str)

    def run(self):
        from datetime import datetime
        hour = datetime.now().hour
        if 6 <= hour < 18:
            self.theme_suggested.emit("velocity")   # Day → Titanium Velocity
        else:
            self.theme_suggested.emit("amethyst")  # Night → Amethyst Noir


class AtmosphereModule(QScrollArea):
    """The full Atmosphere Switcher UI module."""

    theme_changed = pyqtSignal(str)  # emits theme_id for app to re-style

    def __init__(self, logger, parent=None):
        super().__init__(parent)
        self.logger = logger
        self.active_theme_id = load_theme_pref()
        self.setWidgetResizable(True)
        self.setStyleSheet("background: transparent; border: none;")

        content = QWidget()
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        self.main_layout.setSpacing(28)

        self._build_ui()
        self.setWidget(content)

    def _build_ui(self):
        # Header
        self.main_layout.addWidget(make_section(
            "Atmosphere",
            "Choose your identity. Same structure, different soul."
        ))

        # Active indicator
        self.active_lbl = QLabel(f"Active: {THEMES[self.active_theme_id].name}")
        self.active_lbl.setFont(QFont("Inter", 9))
        active_theme = THEMES[self.active_theme_id]
        self.active_lbl.setStyleSheet(f"""
            color: {active_theme.accent};
            background: {active_theme.accent_glow};
            border: 1px solid {active_theme.accent}44;
            border-radius: 8px;
            padding: 6px 14px;
        """)
        self.main_layout.addWidget(self.active_lbl)

        # Theme grid
        grid = QWidget()
        grid_layout = QGridLayout(grid)
        grid_layout.setSpacing(16)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        self.theme_cards: dict[str, ThemeCard] = {}
        positions = [(0,0), (0,1), (0,2), (1,0), (1,1)]

        for (row, col), (tid, theme) in zip(positions, THEMES.items()):
            card = ThemeCard(theme, is_active=(tid == self.active_theme_id))
            card.selected.connect(self._apply_theme)
            grid_layout.addWidget(card, row, col)
            self.theme_cards[tid] = card

        self.main_layout.addWidget(grid)
        self.main_layout.addWidget(make_divider())

        # Auto Scheduler
        self.main_layout.addWidget(make_section(
            "Auto Scheduler",
            "Automatically switch atmosphere by time of day."
        ))

        sched_card = CardFrame()
        sched_layout = QVBoxLayout(sched_card)
        sched_layout.setContentsMargins(20, 16, 20, 16)
        sched_layout.setSpacing(8)

        schedule_info = [
            ("☀️  6:00 – 17:59", "Titanium Velocity", "velocity"),
            ("🌙  18:00 – 5:59", "Amethyst Noir", "amethyst"),
            ("🔋  Battery mode", "Executive Noir (low effects)", "noir"),
        ]
        for time_lbl, theme_name, _ in schedule_info:
            row = QHBoxLayout()
            t_lbl = QLabel(time_lbl)
            t_lbl.setFont(QFont("Inter", 10))
            n_lbl = QLabel(theme_name)
            n_lbl.setFont(QFont("Inter", 9))
            n_lbl.setStyleSheet("color: #6b7585;")
            row.addWidget(t_lbl)
            row.addStretch()
            row.addWidget(n_lbl)
            sched_layout.addLayout(row)

        auto_btn = VaelixButton("Apply Time-Appropriate Theme Now")
        auto_btn.clicked.connect(self._auto_apply)
        sched_layout.addWidget(auto_btn)

        self.main_layout.addWidget(sched_card)
        self.main_layout.addStretch()

    def _apply_theme(self, theme_id: str):
        """Apply chosen theme — live update cards + emit for app re-style."""
        for tid, card in self.theme_cards.items():
            card.setActive(tid == theme_id)

        theme = THEMES[theme_id]
        self.active_lbl.setText(f"Active: {theme.name}")
        self.active_lbl.setStyleSheet(f"""
            color: {theme.accent};
            background: {theme.accent_glow};
            border: 1px solid {theme.accent}44;
            border-radius: 8px;
            padding: 6px 14px;
        """)
        self.active_theme_id = theme_id
        save_theme_pref(theme_id)

        # Apply KDE theme
        subprocess.Popen(
            ["lookandfeeltool", "-a", theme.kde_theme],
            env={**os.environ, "QT_QPA_PLATFORM": "xcb"}
        )

        self.logger.log(f"Atmosphere switched → {theme.name}")
        self.theme_changed.emit(theme_id)

    def _auto_apply(self):
        self.scheduler = AutoScheduler()
        self.scheduler.theme_suggested.connect(self._apply_theme)
        self.scheduler.start()
