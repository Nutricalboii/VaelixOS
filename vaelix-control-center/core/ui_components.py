"""
Shared UI components reused across all modules.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def make_section(title: str, description: str = "") -> QWidget:
    """Returns a polished section widget with title and optional description."""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 4)
    layout.setSpacing(2)

    title_lbl = QLabel(title)
    title_lbl.setFont(QFont("Inter", 13, QFont.Weight.Bold))
    title_lbl.setStyleSheet("color: #e2e8f0;")
    layout.addWidget(title_lbl)

    if description:
        desc_lbl = QLabel(description)
        desc_lbl.setFont(QFont("Inter", 10))
        desc_lbl.setStyleSheet("color: #475569;")
        layout.addWidget(desc_lbl)

    return widget


def make_divider() -> QFrame:
    div = QFrame()
    div.setFixedHeight(1)
    div.setStyleSheet("background: rgba(255,255,255,0.06); margin: 8px 0;")
    return div


class VaelixButton(QPushButton):
    """Standard primary action button."""
    def __init__(self, label: str, color: str = "#3b82f6", parent=None):
        super().__init__(label, parent)
        self.setFont(QFont("Inter", 10, QFont.Weight.DemiBold))
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0 22px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {color}dd;
            }}
            QPushButton:pressed {{
                background: {color}99;
            }}
        """)


class StatusBadge(QLabel):
    """Colored pill badge for showing status."""
    def __init__(self, text: str, color: str = "#3b82f6", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 8, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background: {color}22;
                border: 1px solid {color}44;
                border-radius: 6px;
                padding: 3px 10px;
            }}
        """)

    def set_status(self, text: str, color: str = "#3b82f6"):
        self.setText(text)
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background: {color}22;
                border: 1px solid {color}44;
                border-radius: 6px;
                padding: 3px 10px;
            }}
        """)


class CardFrame(QFrame):
    """A standard dark glass card container."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: rgba(17, 25, 45, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 16px;
            }
        """)


def scrollable_page(inner_widget: QWidget) -> QScrollArea:
    """Wrap a widget in a smooth scrolling area."""
    area = QScrollArea()
    area.setWidgetResizable(True)
    area.setWidget(inner_widget)
    area.setStyleSheet("background: transparent; border: none;")
    return area
