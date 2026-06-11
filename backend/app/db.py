from sqlmodel import SQLModel, create_engine
from sqlalchemy import text

from app.config.path import DB_PATH


engine = None


def get_engine():
    global engine
    if engine is None:
        engine = create_engine(f"sqlite:///{DB_PATH}")
    return engine


def init_db():
    eng = get_engine()

    SQLModel.metadata.create_all(eng)

    with eng.begin() as conn:
        conn.execute(
            text("""
        CREATE VIRTUAL TABLE IF NOT EXISTS snapshot_fts
        USING fts5(
            ocr_text,
            content='snapshot',
            content_rowid='id'
        );
        """)
        )
