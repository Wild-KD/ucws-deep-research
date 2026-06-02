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

from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from config import Config, LLMConfig
from runtime.orchestrator import Orchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("server")

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# In-memory run tracking
runs: dict[str, dict] = {}
run_tasks: dict[str, asyncio.Task] = {}
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

    # ── Health check ──
    @app.get("/healthz")
    async def healthz():
        return {
            "status": "ok",
            "version": "0.1.0",
            "demo": Path("demo").exists(),
            "docs": Path("docs").exists(),
            "skills": len(list(Path("skills").iterdir())) if Path("skills").exists() else 0,
            "active_runs": len([r for r in runs.values() if r.get("status") == "running"]),
        }

    # ── Rate limiting (in-memory, per IP) ──
    request_counts: dict[str, list[float]] = {}
    MAX_REQUESTS_PER_HOUR = 10
    MAX_CONCURRENT_RUNS = 3
    MAX_UPLOAD_SIZE_MB = 20

    def check_rate_limit(ip: str) -> bool:
        import time
        now = time.time()
        if ip not in request_counts:
            request_counts[ip] = []
        request_counts[ip] = [t for t in request_counts[ip] if now - t < 3600]
        if len(request_counts[ip]) >= MAX_REQUESTS_PER_HOUR:
            return False
        request_counts[ip].append(now)
        return True

    # ── API Routes ──

    @app.post("/api/run")
    async def start_run(
        request: Request,
        topic: str = Form(...),
        files: list[UploadFile] = File(default=[]),
        provider: str = Form(default="anthropic"),
        source_urls: str = Form(default=""),
        search_mode: str = Form(default="auto"),
        depth: str = Form(default="standard"),
        language: str = Form(default="bilingual"),
        verification_scope: str = Form(default="key_claims"),
    ):
        """Start a new pipeline run. Upload PDFs and/or let the agent search."""
        client_ip = request.client.host if request.client else "unknown"
        if not check_rate_limit(client_ip):
            return JSONResponse({"error": "Rate limit exceeded (10/hour)"}, status_code=429)

        active = sum(1 for r in runs.values() if r["status"] == "running")
        if active >= MAX_CONCURRENT_RUNS:
            return JSONResponse({"error": "Too many concurrent runs, try later"}, status_code=503)

        run_id = str(uuid.uuid4())[:8]
        run_dir = OUTPUT_DIR / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded files and collect URL sources.
        report_paths = []
        input_sources = []
        for f in files:
            if f.filename and f.filename.lower().endswith(".pdf"):
                safe_name = Path(f.filename).name
                save_path = UPLOAD_DIR / f"{run_id}_{safe_name}"
                content = await f.read()
                if len(content) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
                    return JSONResponse(
                        {"error": f"File too large. Max size is {MAX_UPLOAD_SIZE_MB}MB"},
                        status_code=413,
                    )
                save_path.write_bytes(content)
                report_paths.append(str(save_path))
                input_sources.append({"type": "upload", "name": safe_name, "path": str(save_path)})
                logger.info(f"Saved upload: {save_path} ({len(content)} bytes)")

        urls = [u.strip() for u in source_urls.replace("\r", "\n").split("\n") if u.strip()]
        for url in urls:
            input_sources.append({"type": "url", "url": url})

        runs[run_id] = {
            "id": run_id,
            "topic": topic,
            "provider": provider,
            "status": "pending",
            "progress": [],
            "reports": len(report_paths),
            "urls": len(urls),
            "input_sources": input_sources,
            "config": {
                "search_mode": search_mode,
                "depth": depth,
                "language": language,
                "verification_scope": verification_scope,
            },
            "created_at": datetime.now().isoformat(),
            "output_dir": str(run_dir),
            "error": None,
        }

        # Launch pipeline in background
        run_tasks[run_id] = asyncio.create_task(
            _execute_pipeline(
                run_id,
                topic,
                report_paths,
                provider,
                source_urls=urls,
                run_config=runs[run_id]["config"],
            )
        )

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
        for f in sorted(run_dir.rglob("*")):
            if f.is_file():
                rel = f.relative_to(run_dir).as_posix()
                static_rel = f.relative_to(OUTPUT_DIR).as_posix()
                files.append({"name": rel, "size": f.stat().st_size, "url": f"/output/{static_rel}"})
        return {"run_id": run_id, "files": files}

    @app.get("/api/runs")
    async def list_runs():
        """List all pipeline runs."""
        return {"runs": sorted(runs.values(), key=lambda r: r.get("created_at", ""), reverse=True)}

    @app.post("/api/run/{run_id}/cancel")
    async def cancel_run(run_id: str):
        """Cancel a running pipeline task."""
        if run_id not in runs:
            return JSONResponse({"error": "Run not found"}, status_code=404)
        task = run_tasks.get(run_id)
        if task and not task.done():
            task.cancel()
            runs[run_id]["status"] = "canceled"
            await _broadcast(run_id, {"step": "pipeline", "status": "canceled", "detail": "Run canceled by user"})
        return runs[run_id]

    @app.get("/api/run/{run_id}/artifacts")
    async def list_artifacts(run_id: str):
        """List raw/parsed/manifest artifacts for a run."""
        run_dir = _find_run_dir(run_id)
        if not run_dir:
            return JSONResponse({"error": "Run not found"}, status_code=404)
        artifact_dir = run_dir / "_artifacts"
        artifacts = []
        if artifact_dir.exists():
            for f in sorted(artifact_dir.iterdir()):
                if f.is_file():
                    artifacts.append({"name": f.name, "size": f.stat().st_size, "url": f"/api/run/{run_id}/artifact/{f.name}"})
        return {"run_id": run_id, "artifacts": artifacts}

    @app.get("/api/run/{run_id}/artifact/{artifact_name}")
    async def get_artifact(run_id: str, artifact_name: str):
        """Read a single artifact file."""
        if "/" in artifact_name or "\\" in artifact_name:
            return JSONResponse({"error": "Invalid artifact name"}, status_code=400)
        run_dir = _find_run_dir(run_id)
        if not run_dir:
            return JSONResponse({"error": "Run not found"}, status_code=404)
        path = run_dir / "_artifacts" / artifact_name
        if not path.exists() or not path.is_file():
            return JSONResponse({"error": "Artifact not found"}, status_code=404)
        text = path.read_text(encoding="utf-8")
        if artifact_name.endswith(".json"):
            try:
                return JSONResponse(json.loads(text))
            except json.JSONDecodeError:
                pass
        return HTMLResponse(f"<pre>{_html_escape(text)}</pre>")

    @app.get("/api/run/{run_id}/summary")
    async def get_run_summary(run_id: str):
        """Return an aggregated product-view summary for a run."""
        run_dir = _find_run_dir(run_id)
        if not run_dir:
            return JSONResponse({"error": "Run not found"}, status_code=404)
        return _build_run_summary(run_id, run_dir)

    @app.get("/api/run/{run_id}/source-registry")
    async def get_source_registry(run_id: str):
        """Return distilled source registry if available."""
        run_dir = _find_run_dir(run_id)
        if not run_dir:
            return JSONResponse({"error": "Run not found"}, status_code=404)
        data = _load_first_json(run_dir, ["s4_distill_registry.json", "_artifacts/s4_distill_registry.parsed.json"])
        return {"run_id": run_id, "source_registry": data or {}}

    @app.get("/api/run/{run_id}/dashboard")
    async def get_dashboard_model(run_id: str):
        """Return dashboard model or generated HTML pointer."""
        run_dir = _find_run_dir(run_id)
        if not run_dir:
            return JSONResponse({"error": "Run not found"}, status_code=404)
        files = [p.relative_to(run_dir).as_posix() for p in run_dir.rglob("*.html")]
        data = _load_first_json(run_dir, ["s7_dashboard.json", "_artifacts/s7_dashboard.parsed.json"])
        return {"run_id": run_id, "dashboard": data or {}, "html_files": files}

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


async def _execute_pipeline(
    run_id: str,
    topic: str,
    report_paths: list[str],
    provider: str,
    source_urls: list[str] | None = None,
    run_config: dict | None = None,
):
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
            source_urls=source_urls or None,
            run_config=run_config or {},
            on_progress=on_progress,
        )

        runs[run_id]["status"] = "completed"
        runs[run_id]["result"] = {"run_dir": result["run_dir"]}
        await _broadcast(run_id, {"step": "pipeline", "status": "completed", "detail": "All steps finished"})

    except asyncio.CancelledError:
        runs[run_id]["status"] = "canceled"
        await _broadcast(run_id, {"step": "pipeline", "status": "canceled", "detail": "Run canceled"})
        return
    except Exception as e:
        logger.error(f"Pipeline error for run {run_id}: {e}", exc_info=True)
        runs[run_id]["status"] = "error"
        runs[run_id]["error"] = str(e)
        await _broadcast(run_id, {"step": "pipeline", "status": "error", "detail": str(e)})


def _find_run_dir(run_id: str) -> Path | None:
    if run_id in runs:
        output_dir = runs[run_id].get("output_dir")
        if output_dir:
            direct = Path(output_dir)
            if direct.exists():
                return direct
            matches = list(direct.glob("*")) if direct.exists() else []
            if matches:
                return matches[0]
    direct = OUTPUT_DIR / run_id
    if direct.exists():
        children = [p for p in direct.iterdir() if p.is_dir()]
        if children:
            return sorted(children)[-1]
        return direct
    return None


def _load_first_json(run_dir: Path, names: list[str]):
    for name in names:
        path = run_dir / name
        if path.exists() and path.is_file():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return {"raw": path.read_text(encoding="utf-8")}
    return None


def _build_run_summary(run_id: str, run_dir: Path) -> dict:
    artifacts = []
    artifact_dir = run_dir / "_artifacts"
    if artifact_dir.exists():
        for manifest in sorted(artifact_dir.glob("*.manifest.json")):
            try:
                artifacts.append(json.loads(manifest.read_text(encoding="utf-8")))
            except Exception:
                artifacts.append({"step": manifest.name, "status": "unreadable"})

    outputs = []
    for f in sorted(run_dir.rglob("*")):
        if f.is_file() and "_artifacts" not in f.parts:
            outputs.append({"name": f.relative_to(run_dir).as_posix(), "size": f.stat().st_size})

    return {
        "run_id": run_id,
        "run": runs.get(run_id, {}),
        "run_dir": str(run_dir),
        "artifacts": artifacts,
        "outputs": outputs,
        "source_registry": _load_first_json(run_dir, ["s4_distill_registry.json", "_artifacts/s4_distill_registry.parsed.json"]) or {},
        "merged": _load_first_json(run_dir, ["s5_merged.json", "_artifacts/s5_merged.parsed.json"]) or {},
    }


def _html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


app = create_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 9001))
    uvicorn.run(app, host="0.0.0.0", port=port)
