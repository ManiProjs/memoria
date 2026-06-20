import time
from datetime import datetime, timedelta, timezone
from app.services.capture import capture_screen
from app.services.ocr import extract_text
from app.osapis import get_active_app, get_window_title
from app.db import get_engine
from sqlmodel import Session, select
from app.models import Snapshot
from sqlalchemy import text as sql_text
from hashlib import sha256
from pathlib import Path


def file_hash(path: str) -> str:
    h = sha256()

    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)

    return h.hexdigest()



last_hash = None
last_cleanup_date = None


def cleanup_old_snapshots(days: int = 30):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    with Session(get_engine()) as session:
        old_snapshots = session.exec(
            select(Snapshot).where(Snapshot.timestamp < cutoff)
        ).all()

        for snapshot in old_snapshots:
            try:
                Path(snapshot.image_path).unlink(missing_ok=True)
            except Exception:
                pass

            session.exec(
                sql_text("DELETE FROM snapshot_fts WHERE rowid = :id"),
                {"id": snapshot.id},
            )

            session.delete(snapshot)

        session.commit()


def run_loop(interval: int = 10):
    global last_cleanup_date

    while True:
        global last_hash
        today = datetime.now().date()

        if last_cleanup_date != today:
            cleanup_old_snapshots(30)
            last_cleanup_date = today

        path = capture_screen()
        current_hash = file_hash(path)

        if current_hash == last_hash:
            Path(path).unlink(missing_ok=True)
            print("Skipping duplicate screenshot")
            time.sleep(interval)
            continue

        last_hash = current_hash

        ocr_text = extract_text(path)

        app_name = get_active_app()
        window_title = get_window_title()

        snap = Snapshot(
            image_path=path,
            ocr_text=ocr_text,
            app_name=app_name,
            window_title=window_title
        )

        with Session(get_engine()) as session:
            session.add(snap)
            session.commit()
            session.refresh(snap)

        with get_engine().begin() as conn:
            conn.execute(
                sql_text("INSERT INTO snapshot_fts(rowid, ocr_text) VALUES (:id, :ocr_text)"),
                {"id": snap.id, "ocr_text": snap.ocr_text or ""}
            )

        print("Took screenshot. Path: ", path)

        time.sleep(interval)
