"""
Vaelix Control Center - Main Application Entry Point
PyQt6 | Dark-first | KDE Integrated | Modular
"""

import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QLineEdit, QFrame,
    QScrollArea, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QIcon, QPainter, QLinearGradient, QPen, QPixmap

# Internal module imports
from modules.performance import PerformanceModule
from modules.appearance import AppearanceModule
from modules.graphics import GraphicsModule
from modules.system import SystemModule
from modules.recovery import RecoveryModule
from modules.devtools import DevToolsModule
from modules.atmosphere import AtmosphereModule, load_theme_pref
from core.logger import VaelixLogger
from core.theme_engine import THEMES, get_qt_stylesheet


class SidebarButton(QPushButton):
    """Premium sidebar navigation button with active state and hover animation."""

    def __init__(self, icon_char: str, label: str, parent=None):
        super().__init__(parent)
        self.label_text = label
        self._is_active = False
        self.setFixedHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        # Text only — no flashy icons
        self.setText(f"    {label}")
        self.setFont(QFont("Space Grotesk", 10))
        self._update_style()

    def _update_style(self):
        if self._is_active or self.isChecked():
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(139, 92, 246, 0.10);
                    border: none;
                    border-left: 2px solid #8b5cf6;
                    border-radius: 0;
                    text-align: left;
                    padding-left: 18px;
                    color: #e8e0ff;
                    font-weight: 600;
                    letter-spacing: 0.02em;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    border-left: 2px solid transparent;
                    border-radius: 0;
                    text-align: left;
                    padding-left: 18px;
                    color: #7a7a9a;
                    font-weight: 400;
                }
                QPushButton:hover {
                    background: rgba(139, 92, 246, 0.06);
                    color: #c4b8e8;
                    border-left: 2px solid rgba(139, 92, 246, 0.4);
                }
            """)

    def setActive(self, active: bool):
        self._is_active = active
        self.setChecked(active)
        self._update_style()


class PresetCard(QFrame):
    """One-click mode preset card with hover glow effect."""

    def __init__(self, icon: str, name: str, desc: str, color: str, action_func, parent=None):
        super().__init__(parent)
        self.action_func = action_func
        self.setFixedSize(160, 130)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(30, 41, 59, 0.9),
                    stop:1 rgba(15, 23, 42, 0.95));
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 16px;
            }}
            QFrame:hover {{
                border: 1px solid {color};
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(30, 41, 59, 0.95),
                    stop:1 rgba(15, 23, 42, 0.98));
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Noto Color Emoji", 22))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        name_label = QLabel(name)
        name_label.setFont(QFont("Inter", 9, QFont.Weight.Bold))
        name_label.setStyleSheet(f"color: {color}; border: none; background: transparent;")

        desc_label = QLabel(desc)
        desc_label.setFont(QFont("Inter", 8))
        desc_label.setStyleSheet("color: #64748b; border: none; background: transparent;")
        desc_label.setWordWrap(True)

        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addWidget(desc_label)
        layout.addStretch()

    def mousePressEvent(self, event):
        self.action_func()
        super().mousePressEvent(event)


class HeaderSearch(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("  🔍  Search settings...")
        self.setFixedHeight(38)
        self.setMaximumWidth(320)
        self.setFont(QFont("Inter", 10))
        self.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 0 14px;
                color: #cbd5e1;
            }
            QLineEdit:focus {
                border: 1px solid rgba(59, 130, 246, 0.6);
                background: rgba(255, 255, 255, 0.08);
            }
        """)


class VaelixControlCenter(QMainWindow):
    """Main window for Vaelix Control Center."""

    def __init__(self):
        super().__init__()
        self.logger = VaelixLogger()
        # Default: Amethyst Noir — purple frosted glass identity
        self.active_theme_id = load_theme_pref() or "amethyst"
        self.setWindowTitle("Vaelix Control Center")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)
        self.setWindowFlags(Qt.WindowType.Window)

        self._init_ui()
        self._apply_theme_style(self.active_theme_id)
        self.logger.log("Vaelix Control Center started.")

    def _apply_theme_style(self, theme_id: str):
        """Re-style the entire app when atmosphere changes."""
        self.active_theme_id = theme_id
        theme = THEMES[theme_id]
        base_css = get_qt_stylesheet(theme)
        full_css = f"""
            QMainWindow {{ background: {theme.base_void}; }}
            QWidget {{ background: transparent; color: {theme.text_primary}; font-family: 'Space Grotesk', 'Inter', sans-serif; }}
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{ background: transparent; width: 5px; margin: 0; }}
            QScrollBar::handle:vertical {{ background: {theme.base_border}; border-radius: 2px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """ + base_css
        self.setStyleSheet(full_css)

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(10, 15, 30, 0.98),
                    stop:1 rgba(7, 10, 22, 0.99));
                border-right: 1px solid rgba(255, 255, 255, 0.06);
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 20)
        sidebar_layout.setSpacing(0)

        # Logo area
        logo_widget = QWidget()
        logo_widget.setFixedHeight(72)
        logo_layout = QHBoxLayout(logo_widget)
        logo_layout.setContentsMargins(20, 0, 0, 0)

        logo_label = QLabel("⬡")
        logo_label.setFont(QFont("Inter", 22))
        logo_label.setStyleSheet("color: #3b82f6;")

        brand_col = QVBoxLayout()
        brand_col.setSpacing(0)
        brand_name = QLabel("Vaelix")
        brand_name.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        brand_name.setStyleSheet("color: #f1f5f9;")
        brand_sub = QLabel("Control Center")
        brand_sub.setFont(QFont("Inter", 8))
        brand_sub.setStyleSheet("color: #475569;")
        brand_col.addWidget(brand_name)
        brand_col.addWidget(brand_sub)

        logo_layout.addWidget(logo_label)
        logo_layout.addSpacing(10)
        logo_layout.addLayout(brand_col)
        logo_layout.addStretch()
        sidebar_layout.addWidget(logo_widget)

        # Divider
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet("background: rgba(255,255,255,0.06);")
        sidebar_layout.addWidget(div)
        sidebar_layout.addSpacing(12)

        # Section label
        section_lbl = QLabel("MODULES")
        section_lbl.setFont(QFont("Inter", 8, QFont.Weight.Bold))
        section_lbl.setStyleSheet("color: #334155; padding-left: 20px;")
        sidebar_layout.addWidget(section_lbl)
        sidebar_layout.addSpacing(4)

        # Navigation buttons
        self.nav_buttons = []
        nav_items = [
            ("—", "Atmosphere", 0),
            ("—", "Profiles", 1),
            ("—", "Performance", 2),
            ("—", "Appearance", 3),
            ("—", "Graphics", 4),
            ("—", "System", 5),
            ("—", "Recovery", 6),
            ("—", "Dev Tools", 7),
        ]
        for icon, label, idx in nav_items:
            btn = SidebarButton(icon, label)
            btn.clicked.connect(lambda _, i=idx: self._navigate(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Version label
        ver_lbl = QLabel("v1.0.0 — Vaelix OS")
        ver_lbl.setFont(QFont("Inter", 8))
        ver_lbl.setStyleSheet("color: #1e293b; padding-left: 20px;")
        sidebar_layout.addWidget(ver_lbl)

        # --- MAIN CONTENT ---
        content_area = QWidget()
        content_area.setStyleSheet("background: #111316;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Top Header bar
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet("""
            QFrame {
                background: rgba(10, 15, 30, 0.6);
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(28, 0, 28, 0)

        self.page_title = QLabel("Presets")
        self.page_title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        self.page_title.setStyleSheet("color: #f1f5f9;")

        self.search_bar = HeaderSearch()

        header_layout.addWidget(self.page_title)
        header_layout.addStretch()
        header_layout.addWidget(self.search_bar)
        content_layout.addWidget(header)

        # Stacked pages
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: #111316;")

        atm_module = AtmosphereModule(self.logger)
        atm_module.theme_changed.connect(self._apply_theme_style)

        self.modules = {
            0: atm_module,
            1: self._build_presets_page(),
            2: PerformanceModule(self.logger),
            3: AppearanceModule(self.logger),
            4: GraphicsModule(self.logger),
            5: SystemModule(self.logger),
            6: RecoveryModule(self.logger),
            7: DevToolsModule(self.logger),
        }
        for idx in range(8):
            self.stack.addWidget(self.modules[idx])

        content_layout.addWidget(self.stack)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content_area)

        # Activate first page
        self._navigate(0)

    def _navigate(self, idx: int):
        titles = ["Atmosphere", "Profiles", "Performance", "Appearance", "Graphics", "System", "Recovery", "Dev Tools"]
        self.page_title.setText(titles[idx])
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_buttons):
            btn.setActive(i == idx)

    def _build_presets_page(self) -> QWidget:
        """The legendary one-click preset modes page."""
        page = QScrollArea()
        page.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(32)

        # Hero section
        hero_lbl = QLabel("One-Click Transformations")
        hero_lbl.setFont(QFont("Inter", 28, QFont.Weight.Bold))
        hero_lbl.setStyleSheet("color: #f1f5f9;")

        hero_sub = QLabel("Instantly reshape Vaelix OS to match your task.")
        hero_sub.setFont(QFont("Inter", 13))
        hero_sub.setStyleSheet("color: #475569;")

        layout.addWidget(hero_lbl)
        layout.addWidget(hero_sub)

        # Preset cards grid
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        presets = [
            ("⚡", "Performance X", "Maximum CPU throughput", "#8a9aae", self._preset_gaming),
            ("🔋", "Eco Silent", "Efficiency. Fan quiet.", "#6b8a72", self._preset_battery),
            ("✦", "Studio Flow", "Smooth. Creative. Balanced.", "#7c7aed", self._preset_mac_luxe),
            ("▣", "Atelier", "GPU priority. No interruption.", "#8a7a4a", self._preset_creator),
            ("□", "Quiet Grid", "Distraction removed.", "#4a7a8a", self._preset_focus),
        ]

        for icon, name, desc, color, func in presets:
            card = PresetCard(icon, name, desc, color, func)
            cards_layout.addWidget(card)
        cards_layout.addStretch()
        layout.addLayout(cards_layout)

        # Active state indicator
        self.active_preset_lbl = QLabel("Active: Default")
        self.active_preset_lbl.setFont(QFont("Inter", 10))
        self.active_preset_lbl.setStyleSheet("""
            color: #3b82f6;
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 8px;
            padding: 8px 16px;
        """)
        self.active_preset_lbl.setFixedWidth(200)
        layout.addWidget(self.active_preset_lbl)
        layout.addStretch()

        page.setWidget(content)
        return page

    def _run_as_root(self, cmd: list[str]) -> bool:
        """Run a command with pkexec (PolicyKit GUI auth). Never raw sudo."""
        try:
            result = subprocess.run(["pkexec"] + cmd, capture_output=True, text=True, timeout=30)
            self.logger.log(f"Root cmd: {' '.join(cmd)} → exit {result.returncode}")
            return result.returncode == 0
        except Exception as e:
            self.logger.log(f"Root cmd error: {e}")
            return False

    def _set_cpu_governor(self, governor: str):
        """Switch CPU governor for all cores."""
        cores = os.cpu_count() or 1
        for i in range(cores):
            self._run_as_root(["bash", "-c", f"echo {governor} > /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor"])
        self.logger.log(f"CPU governor → {governor}")

    def _preset_gaming(self):
        self._set_cpu_governor("performance")
        subprocess.run(["kwin_x11", "--replace", "--notifiy-on-start"], capture_output=True)
        self.active_preset_lbl.setText("Active: ⚡ Performance X")
        self.active_preset_lbl.setStyleSheet("""
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
        """)
        self.logger.log("Preset: Gaming Beast activated")

    def _preset_battery(self):
        self._set_cpu_governor("powersave")
        self.active_preset_lbl.setText("Active: 🔋 Eco Silent")
        self.active_preset_lbl.setStyleSheet("""
            color: #22c55e;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
        """)
        self.logger.log("Preset: Battery Monk activated")

    def _preset_mac_luxe(self):
        self._set_cpu_governor("schedutil")
        self.active_preset_lbl.setText("Active: ✨ Studio Flow")
        self.active_preset_lbl.setStyleSheet("""
            color: #a855f7;
            background: rgba(168, 85, 247, 0.1);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
        """)
        self.logger.log("Preset: Mac Luxe activated")

    def _preset_creator(self):
        self._set_cpu_governor("performance")
        self.active_preset_lbl.setText("Active: 🎬 Atelier")
        self.active_preset_lbl.setStyleSheet("""
            color: #f59e0b;
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
        """)
        self.logger.log("Preset: Creator Mode activated")

    def _preset_focus(self):
        self._set_cpu_governor("schedutil")
        self.active_preset_lbl.setText("Active: 🧘 Quiet Grid")
        self.active_preset_lbl.setStyleSheet("""
            color: #06b6d4;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
        """)
        self.logger.log("Preset: Focus Mode activated")


def main():
    os.environ.setdefault("QT_QPA_PLATFORM", "xcb")
    app = QApplication(sys.argv)
    app.setApplicationName("VaelixControlCenter")
    app.setOrganizationName("VaelixOS")

    # Load Inter font if available
    QFont.insertSubstitution("Inter", "Segoe UI")

    window = VaelixControlCenter()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
