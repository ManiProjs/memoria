import time
from app.services.capture import capture_screen
from app.services.ocr import extract_text
from app.db import get_engine
from sqlmodel import Session
from app.models import Snapshot
from sqlalchemy import text as sql_text


def run_loop(interval: int = 10):
    while True:
        path = capture_screen()
        text = extract_text(path)

        snap = Snapshot(image_path=path, ocr_text=text)

        with Session(get_engine()) as session:
            session.add(snap)
            session.commit()
            session.refresh(snap)

        with get_engine().begin() as conn:
            conn.execute(
                sql_text("INSERT INTO snapshot_fts(rowid, ocr_text) VALUES (:id, :text)"),
                {"id": snap.id, "text": snap.ocr_text or ""}
            )

        print("Took screenshot. Path: ", path)

        time.sleep(interval)
