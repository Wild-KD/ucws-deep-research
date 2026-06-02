"""Artifact storage for reproducible agent runs."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class StepArtifact:
    step: str
    status: str
    raw: str | None = None
    parsed: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class ArtifactStore:
    """Writes raw, parsed, and metadata artifacts under a run directory."""

    def __init__(self, run_dir: str | Path):
        self.run_dir = Path(run_dir)
        self.artifact_dir = self.run_dir / "_artifacts"
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

    def write_raw(self, step: str, raw: str) -> Path:
        path = self.artifact_dir / f"{step}.raw.txt"
        path.write_text(raw or "", encoding="utf-8")
        return path

    def write_parsed(self, step: str, parsed: Any) -> Path:
        path = self.artifact_dir / f"{step}.parsed.json"
        path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def write_manifest(self, artifact: StepArtifact) -> Path:
        path = self.artifact_dir / f"{artifact.step}.manifest.json"
        path.write_text(
            json.dumps(asdict(artifact), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def record(
        self,
        step: str,
        *,
        raw: str | None = None,
        parsed: Any = None,
        status: str = "completed",
        error: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> StepArtifact:
        if raw is not None:
            self.write_raw(step, raw)
        if parsed is not None:
            self.write_parsed(step, parsed)
        artifact = StepArtifact(
            step=step,
            status=status,
            raw=raw,
            parsed=parsed,
            error=error,
            metadata=metadata or {},
        )
        self.write_manifest(artifact)
        return artifact

    def load_parsed(self, step: str) -> Any:
        path = self.artifact_dir / f"{step}.parsed.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def list_steps(self) -> list[str]:
        return sorted(p.name.removesuffix(".manifest.json") for p in self.artifact_dir.glob("*.manifest.json"))
