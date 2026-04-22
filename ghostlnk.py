#!/usr/bin/env python3
"""
GhostLNK - Professional LNK Generator with Advanced Evasion
Created by: github.com/Excalibra
Coded for educational and authorized testing purposes only
"""

import sys
from utils.dependencies import ensure_pyqt6, ensure_pylnk3

ensure_pyqt6()
ensure_pylnk3()

from PyQt6.QtWidgets import QApplication
from gui.main_window import GhostLNKGUI

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = GhostLNKGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
