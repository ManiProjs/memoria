import mss
import time
from pathlib import Path
from datetime import datetime, timezone
from app.config.path import SCREENSHOT_DIR
import uuid

def capture_screen():
    with mss.mss() as sct:
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")
        unique_id = uuid.uuid4().hex[:8]

        filename = SCREENSHOT_DIR / f"{timestamp}_{unique_id}.png"

        sct.shot(output=str(filename))
        return str(filename)
