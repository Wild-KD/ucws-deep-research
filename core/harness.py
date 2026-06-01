"""Production harness utilities for validation, replay, and mock runs."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.artifacts import ArtifactStore
from core.json_utils import parse_json_output
from core.schemas import validate_step


@dataclass
class HarnessReport:
    run_dir: str
    steps: list[dict[str, Any]]


class PipelineHarness:
    """Small harness around saved pipeline artifacts.

    The harness is intentionally independent from the full orchestrator so it can
    validate and replay artifacts from failed or offline runs.
    """

    def __init__(self, run_dir: str | Path):
        self.store = ArtifactStore(run_dir)

    def validate(self) -> HarnessReport:
        rows: list[dict[str, Any]] = []
        for step in self.store.list_steps():
            try:
                parsed = self.store.load_parsed(step)
                result = validate_step(step, parsed)
                rows.append({"step": step, "ok": result.ok, "errors": result.errors})
            except Exception as exc:
                rows.append({"step": step, "ok": False, "errors": [str(exc)]})
        return HarnessReport(str(self.store.run_dir), rows)

    def parse_raw_step(self, step: str) -> dict[str, Any]:
        raw_path = self.store.artifact_dir / f"{step}.raw.txt"
        raw = raw_path.read_text(encoding="utf-8")
        parsed = parse_json_output(raw).data
        result = validate_step(step, parsed)
        self.store.record(step, raw=raw, parsed=parsed, status="parsed", metadata={"valid": result.ok})
        return {"step": step, "parsed": parsed, "valid": result.ok, "errors": result.errors}

    def write_report(self, path: str | Path | None = None) -> Path:
        report = self.validate()
        out = Path(path) if path else self.store.run_dir / "harness_report.json"
        out.write_text(json.dumps(report.__dict__, ensure_ascii=False, indent=2), encoding="utf-8")
        return out
