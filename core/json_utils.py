"""Robust JSON extraction and parsing helpers for LLM outputs."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


class JSONExtractionError(ValueError):
    """Raised when no valid JSON object/array can be extracted."""


@dataclass
class ParsedJSON:
    data: Any
    source: str
    repaired: bool = False


FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def extract_json_text(text: str) -> str:
    """Extract a JSON object or array from raw LLM text.

    Handles direct JSON, fenced JSON blocks, and prose-wrapped JSON. This is
    deliberately conservative: it finds balanced top-level object/array text
    rather than guessing at partial structures.
    """
    if not isinstance(text, str) or not text.strip():
        raise JSONExtractionError("empty response")

    raw = text.strip()
    try:
        json.loads(raw)
        return raw
    except Exception:
        pass

    for match in FENCE_RE.finditer(raw):
        candidate = match.group(1).strip()
        try:
            json.loads(candidate)
            return candidate
        except Exception:
            continue

    for opener, closer in (("{", "}"), ("[", "]")):
        start = raw.find(opener)
        if start < 0:
            continue
        depth = 0
        in_string = False
        escape = False
        for idx in range(start, len(raw)):
            ch = raw[idx]
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    candidate = raw[start : idx + 1]
                    try:
                        json.loads(candidate)
                        return candidate
                    except Exception:
                        break

    raise JSONExtractionError("no valid JSON object or array found")


def parse_json_output(text: str) -> ParsedJSON:
    """Parse raw model output into JSON, preserving extraction provenance."""
    extracted = extract_json_text(text)
    return ParsedJSON(
        data=json.loads(extracted),
        source=extracted,
        repaired=(extracted.strip() != text.strip()),
    )


def dumps_pretty(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
