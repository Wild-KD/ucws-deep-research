"""Lightweight runtime schemas for pipeline harness validation.

These are intentionally dependency-free. They do not replace full JSON Schema,
but they catch the structural failures that most often break downstream steps.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class SchemaValidationError(ValueError):
    """Raised when a step artifact does not satisfy the expected contract."""


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)

    def raise_for_errors(self) -> None:
        if not self.ok:
            raise SchemaValidationError("; ".join(self.errors))


def _is_list(value: Any) -> bool:
    return isinstance(value, list)


def _is_dict(value: Any) -> bool:
    return isinstance(value, dict)


def validate_step(step: str, data: Any) -> ValidationResult:
    errors: list[str] = []
    if not _is_dict(data):
        return ValidationResult(False, [f"{step}: expected object, got {type(data).__name__}"])

    if step == "s1_search":
        if "reports" not in data or not _is_list(data["reports"]):
            errors.append("s1_search.reports must be a list")
        else:
            for idx, report in enumerate(data["reports"]):
                if not _is_dict(report):
                    errors.append(f"s1_search.reports[{idx}] must be an object")
                elif not (report.get("file_path") or report.get("url")):
                    errors.append(f"s1_search.reports[{idx}] needs file_path or url")

    elif step.startswith("s2_pyramid"):
        if not any(k in data for k in ("original_pyramid", "reorganized_pyramid", "data_points")):
            errors.append("pyramid output needs original_pyramid, reorganized_pyramid, or data_points")

    elif step.startswith("s3_verified"):
        if "verifications" not in data:
            errors.append("verification output needs verifications")

    elif step == "s4_merged":
        if not any(k in data for k in ("merged_tree", "thesis", "consensus_tree", "nodes")):
            errors.append("merged output needs merged_tree/thesis/consensus_tree/nodes")

    return ValidationResult(ok=not errors, errors=errors)


def validate_or_error(step: str, data: Any) -> None:
    validate_step(step, data).raise_for_errors()
