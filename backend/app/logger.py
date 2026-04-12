import json
import os
from pathlib import Path

from app.config import settings

# In-memory index for fast feedback lookup: query_id -> line number (0-based)
_query_index: dict[str, int] = {}
_log_lines: list[dict] = []


def _ensure_log_dir() -> None:
    Path(settings.log_file).parent.mkdir(parents=True, exist_ok=True)


def _load_existing_log() -> None:
    """Load existing log file into memory on startup."""
    _ensure_log_dir()
    if not os.path.exists(settings.log_file):
        return
    with open(settings.log_file, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                entry = json.loads(line)
                _log_lines.append(entry)
                _query_index[entry["query_id"]] = i


def _flush_log() -> None:
    """Rewrite entire log file from in-memory list."""
    _ensure_log_dir()
    with open(settings.log_file, "w") as f:
        for entry in _log_lines:
            f.write(json.dumps(entry) + "\n")


def log_query(entry: dict) -> None:
    """Append a new query log entry."""
    _ensure_log_dir()
    idx = len(_log_lines)
    _log_lines.append(entry)
    _query_index[entry["query_id"]] = idx
    with open(settings.log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def update_feedback(query_id: str, rating: int, comment: str) -> bool:
    """Update rating and comment for an existing query log entry."""
    if query_id not in _query_index:
        return False
    idx = _query_index[query_id]
    _log_lines[idx]["rating"] = rating
    _log_lines[idx]["comment"] = comment
    _flush_log()
    return True


# Load existing log on module import
_load_existing_log()
