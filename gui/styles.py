STYLESHEET = """
QMainWindow { background-color: #000000; }
QLabel { color: #00FFFF; font-size: 11px; font-family: "Courier New", monospace; }
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #000000;
    color: #00FF00;
    border: 1px solid #FF00FF;
    border-radius: 0px;
    padding: 4px;
    font-size: 11px;
    font-family: "Courier New", monospace;
}
QPushButton {
    background-color: #000000;
    color: #FFFF00;
    border: 1px solid #00FFFF;
    border-radius: 0px;
    padding: 6px;
    font-size: 11px;
    font-weight: bold;
    font-family: "Courier New", monospace;
}
QPushButton:hover { background-color: #333333; }
QGroupBox {
    color: #FF00FF;
    border: 2px solid #00FFFF;
    border-radius: 0px;
    margin-top: 8px;
    font-size: 12px;
    font-weight: bold;
    font-family: "Courier New", monospace;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #FF00FF;
}
QRadioButton, QCheckBox { color: #00FFFF; font-size: 11px; font-family: "Courier New", monospace; }
QTabWidget::pane { border: 1px solid #FF00FF; background-color: #000000; }
QTabBar::tab {
    background-color: #000000;
    color: #FFFF00;
    border: 1px solid #00FFFF;
    padding: 6px 12px;
    margin-right: 2px;
    font-family: "Courier New", monospace;
}
QTabBar::tab:selected { background-color: #333333; color: #FFFFFF; }
QTabBar::tab:hover { background-color: #222222; }
QToolTip {
    background-color: #000000;
    color: #00FF00;
    border: 1px solid #FF00FF;
    padding: 4px;
    font-size: 9px;
    font-family: "Courier New", monospace;
}
QScrollArea { border: none; }

QScrollBar:vertical {
    background: #000000;
    width: 12px;
    border: 1px solid #00FFFF;
}
QScrollBar::handle:vertical {
    background: #00FF00;
    min-height: 20px;
    border: 1px solid #FF00FF;
}
QScrollBar::handle:vertical:hover { background: #33FF33; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: #000000;
    border: 1px solid #00FFFF;
}
QScrollBar:horizontal {
    background: #000000;
    height: 12px;
    border: 1px solid #00FFFF;
}
QScrollBar::handle:horizontal {
    background: #00FF00;
    min-width: 20px;
    border: 1px solid #FF00FF;
}
QScrollBar::handle:horizontal:hover { background: #33FF33; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    background: #000000;
    border: 1px solid #00FFFF;
}
"""
