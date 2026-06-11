from fastapi import APIRouter
from sqlmodel import Session, select
from app.db import get_engine
from app.models import Snapshot

router = APIRouter()


@router.get("/")
def list_snapshots():
    with Session(get_engine()) as session:
        return session.exec(select(Snapshot)).all()
