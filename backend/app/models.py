from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


def now_utc():
    return datetime.now(timezone.utc)

class Snapshot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=now_utc)
    
    app_name: str | None = None
    window_title: str | None = None

    image_path: str
    ocr_text: str | None = None
