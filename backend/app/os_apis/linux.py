import subprocess

def _linux_active_app():
    try:
        return (
            subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"])
            .decode()
            .strip()
        )
    except Exception:
        return None

def _linux_window_title():
    return _linux_active_app()
