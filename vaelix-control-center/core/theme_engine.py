"""
Vaelix Theme Engine
Defines all 5 atmosphere profiles and applies them system-wide.
Same structure. Same spacing. Different soul.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class VaelixTheme:
    """A complete Vaelix atmosphere identity."""
    id: str
    name: str
    tagline: str

    # Base colors
    base_void: str       # Deepest background
    base_primary: str    # Primary app background
    base_panel: str      # Cards, panels
    base_border: str     # Selected border
    base_veil: str       # Dividers, inactive

    # Text
    text_primary: str    # Headings, active
    text_secondary: str  # Body text
    text_muted: str      # Labels, inactive

    # Accent (used sparingly)
    accent: str          # Full-saturation for blade/indicator
    accent_glow: str     # rgba() for glass tint
    accent_hover: str    # rgba() for hover state

    # Session
    wallpaper: str       # Wallpaper filename (in /usr/share/wallpapers/Vaelix/)
    kde_theme: str       # lookandfeeltool theme ID
    blur_strength: int   # 0-100

    # Terminal
    terminal_cursor: str
    terminal_bg: str
    terminal_fg: str


# ─── THE FIVE ATMOSPHERES ────────────────────────────────────────────────────

THEMES: dict[str, VaelixTheme] = {

    "velocity": VaelixTheme(
        id="velocity",
        name="Titanium Velocity",
        tagline="Performance under a calm surface.",

        base_void    = "#080b14",
        base_primary = "#111316",
        base_panel   = "#1c2028",
        base_border  = "#252c3a",
        base_veil    = "#334155",

        text_primary   = "#d4d8e2",
        text_secondary = "#a0aab8",
        text_muted     = "#6b7585",

        accent       = "#7c3aed",
        accent_glow  = "rgba(124,58,237,0.08)",
        accent_hover = "rgba(124,58,237,0.14)",

        wallpaper    = "carbon-breath.jpg",
        kde_theme    = "com.github.vinceliuice.WhiteSur-dark",
        blur_strength = 24,

        terminal_cursor = "#7c3aed",
        terminal_bg     = "#0d1117",
        terminal_fg     = "#c9d1d9",
    ),

    "amethyst": VaelixTheme(
        id="amethyst",
        name="Amethyst Noir",
        tagline="Violet soul in obsidian silence.",

        base_void    = "#07050f",
        base_primary = "#0e0c1a",
        base_panel   = "#171426",
        base_border  = "#311d52",
        base_veil    = "#3e2868",

        # High-contrast text for frosted glass readability
        text_primary   = "#f0ecff",
        text_secondary = "#c4b0e8",
        text_muted     = "#7a6a9a",

        accent       = "#8b5cf6",
        accent_glow  = "rgba(139,92,246,0.09)",   # Reduced — subtle glass tint
        accent_hover = "rgba(139,92,246,0.16)",

        wallpaper    = "velocity-surge.jpg",        # The carbon+violet angular wallpaper
        kde_theme    = "com.github.vinceliuice.WhiteSur-dark",
        blur_strength = 18,                         # Reduced from 32 — still glass, more readable

        terminal_cursor = "#8b5cf6",
        terminal_bg     = "#07050f",
        terminal_fg     = "#ede8ff",                # Bright enough to read easily
    ),

    "noir": VaelixTheme(
        id="noir",
        name="Executive Noir",
        tagline="Wealth does not announce itself.",

        base_void    = "#040406",
        base_primary = "#080808",
        base_panel   = "#111111",
        base_border  = "#2a2118",
        base_veil    = "#3a2f20",

        text_primary   = "#e8dcc8",
        text_secondary = "#a89070",
        text_muted     = "#6a5840",

        accent       = "#b7860b",
        accent_glow  = "rgba(183,134,11,0.07)",
        accent_hover = "rgba(183,134,11,0.12)",

        wallpaper    = "iron-geometry.jpg",
        kde_theme    = "org.kde.breezedark.desktop",
        blur_strength = 16,

        terminal_cursor = "#b7860b",
        terminal_bg     = "#080808",
        terminal_fg     = "#c8b896",
    ),

    "atelier": VaelixTheme(
        id="atelier",
        name="Atelier Midnight",
        tagline="Where craft happens at 3am.",

        base_void    = "#0a0806",
        base_primary = "#100d0a",
        base_panel   = "#1a1512",
        base_border  = "#2e2218",
        base_veil    = "#3d3028",

        text_primary   = "#e0cab4",
        text_secondary = "#a08060",
        text_muted     = "#705840",

        accent       = "#8a6a2a",
        accent_glow  = "rgba(138,106,42,0.09)",
        accent_hover = "rgba(138,106,42,0.16)",

        wallpaper    = "atelier-night.jpg",
        kde_theme    = "org.kde.breezedark.desktop",
        blur_strength = 20,

        terminal_cursor = "#c4962a",
        terminal_bg     = "#0a0806",
        terminal_fg     = "#c8a878",
    ),

    "arctic": VaelixTheme(
        id="arctic",
        name="Arctic Precision",
        tagline="Technical clarity. No warmth wasted.",

        base_void    = "#060c14",
        base_primary = "#0c1320",
        base_panel   = "#141d2e",
        base_border  = "#1e2c42",
        base_veil    = "#2a3d56",

        text_primary   = "#cdd8e8",
        text_secondary = "#8099b4",
        text_muted     = "#405570",

        accent       = "#38bdf8",
        accent_glow  = "rgba(56,189,248,0.07)",
        accent_hover = "rgba(56,189,248,0.13)",

        wallpaper    = "velocity-path.jpg",
        kde_theme    = "org.kde.breezedark.desktop",
        blur_strength = 28,

        terminal_cursor = "#38bdf8",
        terminal_bg     = "#060c14",
        terminal_fg     = "#a8c0d6",
    ),
}

DEFAULT_THEME = "velocity"


def get_theme(theme_id: str) -> VaelixTheme:
    return THEMES.get(theme_id, THEMES[DEFAULT_THEME])


def get_qt_stylesheet(theme: VaelixTheme) -> str:
    """Generate a complete Qt stylesheet for the given theme."""
    a = theme.accent
    ag = theme.accent_glow
    ah = theme.accent_hover

    return f"""
    /* Vaelix Theme Engine — {theme.name} */
    QMainWindow, QDialog {{
        background: {theme.base_void};
    }}
    QWidget {{
        background: transparent;
        color: {theme.text_primary};
        font-family: 'Space Grotesk', 'Inter', sans-serif;
    }}
    /* Sidebar */
    QFrame#sidebar {{
        background: {theme.base_primary};
        border-right: 1px solid {theme.base_veil};
    }}
    /* Active sidebar item — blade only */
    QPushButton[active="true"] {{
        background: {ag};
        border-left: 2px solid {a};
        color: {theme.text_primary};
        font-weight: 600;
    }}
    QPushButton[active="false"]:hover {{
        background: rgba(255,255,255,0.04);
        color: {theme.text_secondary};
    }}
    /* Cards */
    QFrame.card {{
        background: {theme.base_panel};
        border: 1px solid {theme.base_border};
        border-radius: 14px;
    }}
    QFrame.card:hover {{
        border: 1px solid {a};
    }}
    /* Buttons - primary */
    QPushButton.primary {{
        background: {a};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0 20px;
        font-weight: 600;
    }}
    QPushButton.primary:hover {{
        background: {a}dd;
    }}
    /* Buttons - secondary */
    QPushButton.secondary {{
        background: {theme.base_panel};
        color: {theme.text_secondary};
        border: 1px solid {theme.base_border};
        border-radius: 8px;
        padding: 0 16px;
    }}
    QPushButton.secondary:hover {{
        background: {ah};
        border: 1px solid {a};
        color: {theme.text_primary};
    }}
    /* Input fields */
    QLineEdit, QComboBox {{
        background: {theme.base_panel};
        color: {theme.text_primary};
        border: 1px solid {theme.base_border};
        border-radius: 8px;
        padding: 0 12px;
        selection-background-color: {ag};
    }}
    QLineEdit:focus, QComboBox:focus {{
        border: 1px solid {a};
    }}
    /* Progress bar */
    QProgressBar {{
        background: {theme.base_panel};
        border-radius: 4px;
        border: none;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
            stop:0 {a}, stop:1 {a}88);
        border-radius: 4px;
    }}
    /* Scrollbar */
    QScrollBar:vertical {{
        background: transparent;
        width: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {theme.base_border};
        border-radius: 2px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    /* Slider */
    QSlider::groove:horizontal {{
        height: 3px;
        background: {theme.base_border};
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {a};
        width: 14px; height: 14px;
        border-radius: 7px;
        margin: -6px 0;
    }}
    QSlider::sub-page:horizontal {{
        background: {a};
        border-radius: 2px;
    }}
    /* Status badges */
    QLabel.badge {{
        color: {a};
        background: {ag};
        border: 1px solid {a}44;
        border-radius: 6px;
        padding: 2px 10px;
    }}
    """
