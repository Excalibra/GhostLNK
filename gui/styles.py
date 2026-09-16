COLOR_BG = "#0b0b0d"
COLOR_PANEL = "#131316"
COLOR_INPUT = "#0a0a0c"
COLOR_BORDER = "#2a2a31"
COLOR_BORDER_HOVER = "#4a4a55"
COLOR_TEXT = "#d7d7dc"
COLOR_MUTED = "#84848c"
COLOR_FAINT = "#55555e"
COLOR_ACCENT = "#b3292e"
COLOR_ACCENT_DIM = "#6e1b1f"
COLOR_SUCCESS = "#7da07a"
COLOR_WARNING = "#c9a227"

FONT_MAIN = '"Segoe UI", "Helvetica Neue", "DejaVu Sans", sans-serif'
FONT_MONO = '"Cascadia Mono", "Consolas", "DejaVu Sans Mono", monospace'

STYLESHEET = f"""
QMainWindow, QDialog, QMessageBox {{
    background-color: {COLOR_BG};
}}
QWidget {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT};
    font-family: {FONT_MAIN};
    font-size: 12px;
}}
QLabel {{
    color: {COLOR_TEXT};
    background-color: transparent;
    font-size: 12px;
}}
QLineEdit, QTextEdit, QComboBox, QSpinBox {{
    background-color: {COLOR_INPUT};
    color: {COLOR_TEXT};
    border: 1px solid {COLOR_BORDER};
    border-radius: 2px;
    padding: 5px 7px;
    selection-background-color: {COLOR_ACCENT_DIM};
    selection-color: #f0f0f2;
}}
QLineEdit:hover, QTextEdit:hover, QComboBox:hover, QSpinBox:hover {{
    border: 1px solid {COLOR_BORDER_HOVER};
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 1px solid {COLOR_ACCENT};
}}
QLineEdit:disabled, QTextEdit:disabled, QComboBox:disabled, QSpinBox:disabled {{
    color: {COLOR_FAINT};
    border: 1px solid #1d1d22;
    background-color: #0d0d0f;
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {COLOR_MUTED};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXT};
    border: 1px solid {COLOR_BORDER};
    selection-background-color: {COLOR_ACCENT_DIM};
    selection-color: #f0f0f2;
    outline: none;
}}
QPushButton {{
    background-color: #17171b;
    color: {COLOR_TEXT};
    border: 1px solid {COLOR_BORDER};
    border-radius: 2px;
    padding: 6px 14px;
    font-size: 12px;
}}
QPushButton:hover {{
    background-color: #1e1e24;
    border: 1px solid {COLOR_BORDER_HOVER};
}}
QPushButton:pressed {{
    background-color: {COLOR_ACCENT_DIM};
    border: 1px solid {COLOR_ACCENT};
    color: #f0f0f2;
}}
QPushButton:disabled {{
    color: {COLOR_FAINT};
    border: 1px solid #1d1d22;
    background-color: #101013;
}}
QGroupBox {{
    color: {COLOR_MUTED};
    background-color: {COLOR_PANEL};
    border: 1px solid {COLOR_BORDER};
    border-radius: 3px;
    margin-top: 14px;
    padding-top: 6px;
    font-size: 11px;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 6px;
    color: {COLOR_MUTED};
    background-color: {COLOR_PANEL};
}}
QRadioButton, QCheckBox {{
    color: {COLOR_TEXT};
    background-color: transparent;
    spacing: 7px;
    font-size: 12px;
}}
QRadioButton:disabled, QCheckBox:disabled {{
    color: {COLOR_FAINT};
}}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 14px;
    height: 14px;
    background-color: {COLOR_INPUT};
    border: 1px solid {COLOR_BORDER};
}}
QCheckBox::indicator {{
    border-radius: 2px;
}}
QRadioButton::indicator {{
    border-radius: 7px;
}}
QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
    border: 1px solid {COLOR_BORDER_HOVER};
}}
QCheckBox::indicator:checked {{
    background-color: {COLOR_ACCENT};
    border: 1px solid {COLOR_ACCENT};
    image: none;
}}
QRadioButton::indicator:checked {{
    background-color: {COLOR_ACCENT};
    border: 1px solid {COLOR_ACCENT};
}}
QCheckBox::indicator:disabled, QRadioButton::indicator:disabled {{
    background-color: #101013;
    border: 1px solid #1d1d22;
}}
QListWidget {{
    background-color: {COLOR_INPUT};
    color: {COLOR_MUTED};
    border: 1px solid {COLOR_BORDER};
    border-radius: 2px;
    font-family: {FONT_MONO};
    font-size: 11px;
    outline: none;
}}
QListWidget::item {{
    padding: 3px 6px;
}}
QListWidget::item:selected {{
    background-color: {COLOR_ACCENT_DIM};
    color: #f0f0f2;
}}
QListWidget::item:hover {{
    background-color: #1a1a1f;
}}
QTabWidget::pane {{
    border: 1px solid {COLOR_BORDER};
    background-color: {COLOR_PANEL};
}}
QTabBar::tab {{
    background-color: {COLOR_BG};
    color: {COLOR_MUTED};
    border: 1px solid {COLOR_BORDER};
    border-bottom: none;
    padding: 6px 14px;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXT};
    border-top: 2px solid {COLOR_ACCENT};
}}
QTabBar::tab:hover:!selected {{
    background-color: #17171b;
    color: {COLOR_TEXT};
}}
QToolTip {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXT};
    border: 1px solid {COLOR_BORDER};
    padding: 5px 7px;
    font-size: 11px;
}}
QScrollArea {{
    background-color: {COLOR_BG};
    border: none;
}}
QSplitter::handle {{
    background-color: {COLOR_BG};
}}
QSplitter::handle:horizontal {{
    width: 4px;
}}
QSplitter::handle:vertical {{
    height: 4px;
}}
QSplitter::handle:hover {{
    background-color: {COLOR_ACCENT_DIM};
}}
QScrollBar:vertical {{
    background: {COLOR_BG};
    width: 10px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #2e2e36;
    min-height: 24px;
    border-radius: 4px;
    margin: 2px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLOR_BORDER_HOVER};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: {COLOR_BG};
    height: 10px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: #2e2e36;
    min-width: 24px;
    border-radius: 4px;
    margin: 2px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {COLOR_BORDER_HOVER};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
QScrollBar::add-page, QScrollBar::sub-page {{
    background: none;
}}
QMenuBar {{
    background-color: {COLOR_BG};
    color: {COLOR_MUTED};
    border-bottom: 1px solid #1d1d22;
}}
QMenuBar::item {{
    background-color: transparent;
    padding: 5px 10px;
}}
QMenuBar::item:selected {{
    color: {COLOR_TEXT};
    background-color: #1a1a1f;
}}
QMenu {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXT};
    border: 1px solid {COLOR_BORDER};
}}
QMenu::item {{
    padding: 6px 24px 6px 12px;
}}
QMenu::item:selected {{
    background-color: {COLOR_ACCENT_DIM};
    color: #f0f0f2;
}}
QStatusBar {{
    background-color: {COLOR_BG};
    color: {COLOR_FAINT};
    border-top: 1px solid #1d1d22;
    font-size: 11px;
}}
QFileDialog, QFileDialog QListView, QFileDialog QTreeView {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXT};
}}
"""
