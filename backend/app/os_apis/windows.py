import subprocess
import psutil

def _windows_active_app():
    try:
        import win32gui
        import win32process

        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        return psutil.Process(pid).name()
    except:
        return None


def _windows_window_title():
    try:
        import win32gui

        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return None
