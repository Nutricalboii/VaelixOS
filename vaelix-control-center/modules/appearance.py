"""
Appearance Module — Theme, accent colors, blur, fonts, dock position.
"""
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QComboBox, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from core.ui_components import make_section, make_divider, VaelixButton, CardFrame


ACCENTS = {
    "Vaelix Blue":  "#3b82f6",
    "Royal Purple": "#a855f7",
    "Crimson Red":  "#ef4444",
    "Emerald":      "#22c55e",
    "Amber":        "#f59e0b",
    "Cyan":         "#06b6d4",
    "Rose":         "#f43f5e",
    "Graphite":     "#6b7280",
}


class AccentDot(QWidget):
    selected = pyqtSignal(str, str)  # name, hex

    def __init__(self, name: str, hex_color: str, parent=None):
        super().__init__(parent)
        self.name = name
        self.hex_color = hex_color
        self.setFixedSize(40, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._active = False

    def setActive(self, active: bool):
        self._active = active
        self.update()

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QBrush, QPen
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(self.hex_color)
        painter.setBrush(QBrush(color))
        if self._active:
            painter.setPen(QPen(QColor("white"), 2))
        else:
            painter.setPen(QPen(QColor("transparent"), 0))
        painter.drawEllipse(4, 4, 32, 32)

    def mousePressEvent(self, event):
        self.selected.emit(self.name, self.hex_color)


class AppearanceModule(QScrollArea):
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
        # Accent Color
        self.main_layout.addWidget(make_section(
            "Accent Color",
            "Select the signature color for Vaelix OS."
        ))

        accent_card = CardFrame()
        accent_layout = QVBoxLayout(accent_card)
        accent_layout.setContentsMargins(20, 16, 20, 16)

        dots_row = QHBoxLayout()
        dots_row.setSpacing(12)
        self.accent_dots = {}
        for name, color in ACCENTS.items():
            dot = AccentDot(name, color)
            dot.selected.connect(self._apply_accent)
            self.accent_dots[name] = dot
            dots_row.addWidget(dot)
        dots_row.addStretch()

        self.accent_label = QLabel("Selected: Vaelix Blue")
        self.accent_label.setFont(QFont("Inter", 9))
        self.accent_label.setStyleSheet("color: #3b82f6;")

        self.accent_dots["Vaelix Blue"].setActive(True)
        accent_layout.addLayout(dots_row)
        accent_layout.addWidget(self.accent_label)
        self.main_layout.addWidget(accent_card)

        self.main_layout.addWidget(make_divider())

        # Theme Switcher
        self.main_layout.addWidget(make_section(
            "Desktop Theme",
            "Switch between available Plasma global themes."
        ))

        theme_card = CardFrame()
        theme_layout = QHBoxLayout(theme_card)
        theme_layout.setContentsMargins(20, 16, 20, 16)
        theme_layout.setSpacing(12)

        theme_lbl = QLabel("Theme:")
        theme_lbl.setFont(QFont("Inter", 10))

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["WhiteSur Dark", "Breeze Dark", "Breeze Light", "Breeze Twilight"])
        self.theme_combo.setFixedHeight(36)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 0 12px;
                color: #cbd5e1;
            }
            QComboBox::drop-down { border: none; }
        """)

        apply_btn = VaelixButton("Apply Theme")
        apply_btn.clicked.connect(self._apply_theme)

        theme_layout.addWidget(theme_lbl)
        theme_layout.addWidget(self.theme_combo, 1)
        theme_layout.addWidget(apply_btn)
        self.main_layout.addWidget(theme_card)

        self.main_layout.addWidget(make_divider())

        # Blur Strength & Animation Speed
        self.main_layout.addWidget(make_section(
            "Visual Effects",
            "Fine-tune blur and animation speed."
        ))

        fx_card = CardFrame()
        fx_layout = QVBoxLayout(fx_card)
        fx_layout.setContentsMargins(20, 16, 20, 20)
        fx_layout.setSpacing(16)

        for label, default_val in [("Blur Strength", 70), ("Animation Speed", 60)]:
            row_layout = QVBoxLayout()
            row_layout.setSpacing(4)

            top = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setFont(QFont("Inter", 10))
            val_lbl = QLabel(f"{default_val}%")
            val_lbl.setFont(QFont("Inter", 9))
            val_lbl.setStyleSheet("color: #3b82f6;")
            top.addWidget(lbl)
            top.addStretch()
            top.addWidget(val_lbl)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(default_val)
            slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    height: 4px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 2px;
                }
                QSlider::handle:horizontal {
                    background: #3b82f6;
                    width: 16px; height: 16px;
                    border-radius: 8px;
                    margin: -6px 0;
                }
                QSlider::sub-page:horizontal {
                    background: #3b82f6;
                    border-radius: 2px;
                }
            """)
            slider.valueChanged.connect(lambda v, lbl=val_lbl: lbl.setText(f"{v}%"))

            row_layout.addLayout(top)
            row_layout.addWidget(slider)
            fx_layout.addLayout(row_layout)

        self.main_layout.addWidget(fx_card)

        # Font preset
        self.main_layout.addWidget(make_divider())
        self.main_layout.addWidget(make_section("Font Preset", "Change system-wide font."))

        font_card = CardFrame()
        font_layout = QHBoxLayout(font_card)
        font_layout.setContentsMargins(20, 16, 20, 16)

        font_combo = QComboBox()
        font_combo.addItems(["Inter (Vaelix Default)", "Noto Sans", "Ubuntu", "Roboto", "System Default"])
        font_combo.setFixedHeight(36)
        font_combo.setStyleSheet(self.theme_combo.styleSheet())

        font_apply = VaelixButton("Apply Font")
        font_layout.addWidget(QLabel("Font:"))
        font_layout.addWidget(font_combo, 1)
        font_layout.addWidget(font_apply)
        self.main_layout.addWidget(font_card)

        self.main_layout.addStretch()

    def _apply_accent(self, name: str, color: str):
        for n, dot in self.accent_dots.items():
            dot.setActive(n == name)
        self.accent_label.setText(f"Selected: {name}")
        self.accent_label.setStyleSheet(f"color: {color};")
        self.logger.log(f"Accent color → {name} ({color})")

    def _apply_theme(self):
        theme_map = {
            "WhiteSur Dark": "com.github.vinceliuice.WhiteSur-dark",
            "Breeze Dark": "org.kde.breezedark.desktop",
            "Breeze Light": "org.kde.breeze.desktop",
            "Breeze Twilight": "org.kde.breezetwilight.desktop",
        }
        selected = self.theme_combo.currentText()
        theme_id = theme_map.get(selected, "org.kde.breezedark.desktop")
        subprocess.Popen(
            ["lookandfeeltool", "-a", theme_id],
            env={"QT_QPA_PLATFORM": "xcb", "DISPLAY": ":0", "HOME": "/root"}
        )
        self.logger.log(f"Theme applied → {theme_id}")
