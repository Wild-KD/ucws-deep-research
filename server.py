"""
FastAPI server for serving the demo and (optionally) running the pipeline.
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


def create_app(demo_dir: str = "demo") -> FastAPI:
    app = FastAPI(
        title="Investment Research Logic Engine",
        description="A Deep Research Agent that audits investment thesis logic",
        version="0.1.0",
    )

    demo_path = Path(demo_dir)

    @app.get("/")
    async def index():
        return RedirectResponse(url="/demo/index.html")

    if demo_path.exists():
        app.mount("/demo", StaticFiles(directory=str(demo_path), html=True), name="demo")

    return app


if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
