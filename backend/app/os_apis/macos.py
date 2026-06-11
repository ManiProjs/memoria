import subprocess

def _mac_active_app():
    try:
        script = 'tell application "System Events" to get name of first application process whose frontmost is true'
        return subprocess.check_output(["osascript", "-e", script]).decode().strip()
    except Exception:
        return None


def _mac_window_title():
    try:
        script = """
        tell application "System Events"
            tell process (name of first application process whose frontmost is true)
                try
                    return name of front window
                end try
            end tell
        end tell
        """
        return subprocess.check_output(["osascript", "-e", script]).decode().strip()
    except Exception:
        return None
