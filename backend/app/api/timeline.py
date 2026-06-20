from fastapi import APIRouter
from sqlmodel import Session, select
from app.db import get_engine
from app.models import Snapshot

router = APIRouter()


@router.get("/")
def timeline(limit: int = 50, offset: int = 0):
    with Session(get_engine()) as session:
        stmt = (
            select(Snapshot)
            .order_by(Snapshot.timestamp.desc())
            .offset(offset)
            .limit(limit)
        )
        return session.exec(stmt).all()
