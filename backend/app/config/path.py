from platformdirs import user_data_dir
from pathlib import Path

APP_NAME = "memoria"
APP_AUTHOR = "com.maniarasteh"

BASE_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))

SCREENSHOT_DIR = BASE_DIR / "screenshots"
DB_PATH = BASE_DIR / "memoria.db"
LOG_DIR = BASE_DIR / "logs"


def ensure_dirs():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    BASE_DIR.mkdir(parents=True, exist_ok=True)
