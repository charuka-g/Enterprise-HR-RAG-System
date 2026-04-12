import os
import hashlib
from datetime import datetime
from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".html", ".htm", ".txt"}


def _parse_metadata_from_path(rel_path: str) -> dict:
    """Parse business_unit, country, acl_groups from folder structure."""
    parts = Path(rel_path).parts
    # parts[0] is the immediate subfolder under docs/
    if len(parts) < 2:
        return {"business_unit": "general", "country": "global", "acl_groups": ["all"]}

    top_folder = parts[0]

    # Convention: docs/BU_Finance/LK/file.pdf
    if top_folder.startswith("BU_"):
        business_unit = top_folder[3:]  # strip "BU_" prefix
        country = parts[1] if len(parts) >= 3 else "global"
        acl_groups = [business_unit]
        return {"business_unit": business_unit, "country": country, "acl_groups": acl_groups}

    # Convention: docs/global/file.pdf
    if top_folder.lower() == "global":
        return {"business_unit": "global", "country": "global", "acl_groups": ["all"]}

    return {"business_unit": "general", "country": "global", "acl_groups": ["all"]}


def _doc_type(extension: str) -> str:
    mapping = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".doc": "docx",
        ".html": "html",
        ".htm": "html",
        ".txt": "txt",
    }
    return mapping.get(extension.lower(), "txt")


def discover_docs(docs_dir: str) -> list[dict]:
    """Walk docs_dir and return a list of document dicts."""
    docs = []
    docs_path = Path(docs_dir)

    for file_path in sorted(docs_path.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        rel_path = file_path.relative_to(docs_path)
        rel_path_str = str(rel_path)

        # Stable doc_id from file path hash
        doc_id = hashlib.md5(rel_path_str.encode()).hexdigest()

        metadata = _parse_metadata_from_path(rel_path_str)
        last_updated = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()

        with open(file_path, "rb") as f:
            raw_bytes = f.read()

        docs.append({
            "doc_id": doc_id,
            "file_path": rel_path_str,
            "file_name": file_path.name,
            "doc_type": _doc_type(file_path.suffix),
            "business_unit": metadata["business_unit"],
            "country": metadata["country"],
            "acl_groups": metadata["acl_groups"],
            "last_updated": last_updated,
            "raw_bytes": raw_bytes,
        })

    return docs
