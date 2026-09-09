from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from backend.api.analyze import analyze_screenshot
from backend.api.history import get_history
from backend.api.backtest import run_backtest
from backend.api.results import import_results

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="EdgeLens Pro",
    version="1.0.0",
    description="Screenshot-based sports analytics platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/status")
def status():
    return {
        "status": "online",
        "service": "EdgeLens Pro"
    }


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    return analyze_screenshot(contents)


@app.get("/api/history")
def history():
    return get_history()


@app.post("/api/backtest")
def backtest():
    return run_backtest()


@app.post("/api/results/import")
async def results_import(file: UploadFile = File(...)):
    contents = await file.read()
    return import_results(contents)


@app.get("/")
def frontend():
    return FileResponse(
        BASE_DIR / "frontend" / "index.html"
    )