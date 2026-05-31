"""
Production FastAPI server for the Investment Research Logic Engine.
Handles file uploads, pipeline execution, progress streaming, and result serving.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from config import Config, LLMConfig
from core.orchestrator import Orchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("server")

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# In-memory run tracking
runs: dict[str, dict] = {}
# WebSocket connections per run
ws_connections: dict[str, list[WebSocket]] = {}


def create_app() -> FastAPI:
    app = FastAPI(
        title="Investment Research Logic Engine",
        description="Deep Research Agent that audits investment thesis logic",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── API Routes ──

    @app.post("/api/run")
    async def start_run(
        topic: str = Form(...),
        files: list[UploadFile] = File(default=[]),
        provider: str = Form(default="anthropic"),
    ):
        """Start a new pipeline run. Upload PDFs and/or let the agent search."""
        run_id = str(uuid.uuid4())[:8]
        run_dir = OUTPUT_DIR / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded files
        report_paths = []
        for f in files:
            if f.filename and f.filename.endswith(".pdf"):
                save_path = UPLOAD_DIR / f"{run_id}_{f.filename}"
                content = await f.read()
                save_path.write_bytes(content)
                report_paths.append(str(save_path))
                logger.info(f"Saved upload: {save_path} ({len(content)} bytes)")

        runs[run_id] = {
            "id": run_id,
            "topic": topic,
            "provider": provider,
            "status": "pending",
            "progress": [],
            "reports": len(report_paths),
            "created_at": datetime.now().isoformat(),
            "output_dir": str(run_dir),
            "error": None,
        }

        # Launch pipeline in background
        asyncio.create_task(_execute_pipeline(run_id, topic, report_paths, provider))

        return {"run_id": run_id, "status": "started"}

    @app.get("/api/run/{run_id}")
    async def get_run(run_id: str):
        """Get the status and progress of a pipeline run."""
        if run_id not in runs:
            return JSONResponse({"error": "Run not found"}, status_code=404)
        return runs[run_id]

    @app.get("/api/run/{run_id}/outputs")
    async def get_outputs(run_id: str):
        """List output files for a completed run."""
        run_dir = OUTPUT_DIR / run_id
        if not run_dir.exists():
            return JSONResponse({"error": "Output not found"}, status_code=404)
        files = []
        for f in sorted(run_dir.iterdir()):
            files.append({"name": f.name, "size": f.stat().st_size, "url": f"/output/{run_id}/{f.name}"})
        return {"run_id": run_id, "files": files}

    @app.get("/api/runs")
    async def list_runs():
        """List all pipeline runs."""
        return {"runs": list(runs.values())}

    @app.websocket("/ws/{run_id}")
    async def websocket_progress(websocket: WebSocket, run_id: str):
        """WebSocket endpoint for real-time progress updates."""
        await websocket.accept()
        if run_id not in ws_connections:
            ws_connections[run_id] = []
        ws_connections[run_id].append(websocket)

        # Send current progress history
        if run_id in runs:
            for msg in runs[run_id].get("progress", []):
                await websocket.send_json(msg)

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            ws_connections[run_id].remove(websocket)

    # ── Static file serving ──

    @app.get("/", response_class=HTMLResponse)
    async def index():
        index_path = Path("docs/index.html")
        if index_path.exists():
            return index_path.read_text(encoding="utf-8")
        return "<h1>Investment Research Logic Engine</h1><p>docs/index.html not found</p>"

    # Serve output files
    output_path = Path("output")
    output_path.mkdir(exist_ok=True)
    app.mount("/output", StaticFiles(directory="output", html=True), name="output")

    # Serve demo files
    demo_path = Path("demo")
    if demo_path.exists():
        app.mount("/demo", StaticFiles(directory="demo", html=True), name="demo")

    # Serve docs (landing page assets)
    docs_path = Path("docs")
    if docs_path.exists():
        app.mount("/docs", StaticFiles(directory="docs", html=True), name="docs")

    return app


async def _broadcast(run_id: str, message: dict):
    """Send a progress message to all WebSocket clients for this run."""
    if run_id in ws_connections:
        dead = []
        for ws in ws_connections[run_id]:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            ws_connections[run_id].remove(ws)


async def _execute_pipeline(run_id: str, topic: str, report_paths: list[str], provider: str):
    """Execute the full pipeline and stream progress via WebSocket."""
    try:
        runs[run_id]["status"] = "running"

        config = Config(
            llm=LLMConfig.from_env(provider),
            output_dir=f"output/{run_id}",
        )
        orchestrator = Orchestrator(config)

        async def on_progress(step: str, status: str, detail: str = ""):
            msg = {
                "step": step,
                "status": status,
                "detail": detail,
                "timestamp": datetime.now().isoformat(),
            }
            runs[run_id]["progress"].append(msg)
            await _broadcast(run_id, msg)

        result = await orchestrator.run(
            topic=topic,
            report_paths=report_paths if report_paths else None,
            on_progress=on_progress,
        )

        runs[run_id]["status"] = "completed"
        runs[run_id]["result"] = {"run_dir": result["run_dir"]}
        await _broadcast(run_id, {"step": "pipeline", "status": "completed", "detail": "All steps finished"})

    except Exception as e:
        logger.error(f"Pipeline error for run {run_id}: {e}", exc_info=True)
        runs[run_id]["status"] = "error"
        runs[run_id]["error"] = str(e)
        await _broadcast(run_id, {"step": "pipeline", "status": "error", "detail": str(e)})


app = create_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 9001))
    uvicorn.run(app, host="0.0.0.0", port=port)
