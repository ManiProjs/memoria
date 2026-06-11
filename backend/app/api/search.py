from fastapi import APIRouter, Query
from sqlalchemy import text
from app.db import get_engine

router = APIRouter()


@router.get("/")
def search(q: str = Query(...)):
    with get_engine().begin() as conn:
        results = conn.execute(
            text("""
            SELECT snapshot.rowid, snapshot.*
            FROM snapshot_fts
            JOIN snapshot ON snapshot.id = snapshot_fts.rowid
            WHERE snapshot_fts MATCH :q
            ORDER BY rank
            LIMIT 50
            """),
            {"q": q},
        ).fetchall()

    return {"query": q, "results": [dict(r._mapping) for r in results]}
