import platform
from app.os_apis.windows import _windows_window_title, _windows_active_app
from app.os_apis.macos import _mac_window_title, _mac_active_app
from app.os_apis.linux import _linux_window_title, _linux_active_app

def get_active_app():
    os_name = platform.system()

    if os_name == "Darwin":
        return _mac_active_app()
    elif os_name == "Windows":
        return _windows_active_app()
    else:
        return _linux_active_app()


def get_window_title():
    os_name = platform.system()

    if os_name == "Darwin":
        return _mac_window_title()
    elif os_name == "Windows":
        return _windows_window_title()
    else:
        return _linux_window_title()
