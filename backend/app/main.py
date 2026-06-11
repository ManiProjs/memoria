from fastapi import FastAPI
from app.db import init_db
from app.api import snapshots, search, timeline, health
from app.services.index import run_loop
from app.config.path import ensure_dirs
from contextlib import asynccontextmanager
import threading

def start_worker():
    def worker():
        run_loop(interval=10)
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_dirs()
    # startup
    init_db()
    start_worker()
    yield  # app runs here
    # shutdown (optional cleanup later)


app = FastAPI(title="Memoria", lifespan=lifespan)

app.include_router(health.router)
app.include_router(snapshots.router, prefix="/snapshots")
app.include_router(search.router, prefix="/search")
app.include_router(timeline.router, prefix="/timeline")
