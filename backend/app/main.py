from fastapi import FastAPI
from app.db import init_db
from app.api import snapshots, search, timeline, health
from app.services.index import run_loop
from app.config.path import ensure_dirs
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config.path import SCREENSHOT_DIR
import threading
import os


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


app.add_middleware(
    CORSMiddleware,
    # If you want to use your own port, you must add it here.
    allow_origins=[
        "http://localhost:5173", # Dev server
        "http://localhost:4173"  # `npm run preview`
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/screenshots")
def list_screenshots():
    files = os.listdir(SCREENSHOT_DIR)
    return {
        "screenshots": [
            f for f in files if f.endswith((".png", ".jpg", ".jpeg"))
        ]
    }

app.include_router(health.router)
app.include_router(snapshots.router, prefix="/snapshots")
app.include_router(search.router, prefix="/search")
app.include_router(timeline.router, prefix="/timeline")
app.mount("/screenshots", StaticFiles(directory=SCREENSHOT_DIR), name="screenshots")
