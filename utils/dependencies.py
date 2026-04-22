import sys
import subprocess

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
