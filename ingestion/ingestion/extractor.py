import io
import re
from collections import Counter


def _clean_text(text: str) -> str:
    """Normalize whitespace, line breaks, and strip boilerplate dividers."""
    # Collapse multiple spaces/tabs to single space
    text = re.sub(r"[ \t]+", " ", text)
    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.splitlines()]
    # Remove lines that are purely dashes, underscores, or equals signs
    lines = [line for line in lines if not re.fullmatch(r"[-_=]{2,}", line)]
    # Collapse 3+ consecutive newlines to 2
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_pdf(raw_bytes: bytes) -> str:
    import pdfplumber

    all_pages = []
    line_counter: Counter = Counter()

    with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
        # First pass: count repeated short lines (headers/footers)
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            for line in page_text.splitlines():
                line = line.strip()
                if line and len(line) < 20:
                    line_counter[line] += 1

        repeated_lines = {line for line, count in line_counter.items() if count >= 3}

        # Second pass: extract text, skipping repeated short lines
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            filtered = []
            for line in page_text.splitlines():
                stripped = line.strip()
                if stripped in repeated_lines:
                    continue
                filtered.append(stripped)
            all_pages.append("\n".join(filtered))

    return "\n".join(all_pages)


def _extract_docx(raw_bytes: bytes) -> str:
    import docx

    doc = docx.Document(io.BytesIO(raw_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def _extract_html(raw_bytes: bytes) -> str:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(raw_bytes, "html.parser")
    # Remove noise tags
    for tag in soup.find_all(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    body = soup.find("body")
    return (body or soup).get_text(separator="\n")


def _extract_txt(raw_bytes: bytes) -> str:
    return raw_bytes.decode("utf-8", errors="replace")


_EXTRACTORS = {
    "pdf": _extract_pdf,
    "docx": _extract_docx,
    "html": _extract_html,
    "txt": _extract_txt,
}


def extract_text(doc: dict) -> dict:
    """Extract and clean text from a doc dict. Returns dict with full_text and metadata."""
    doc_type = doc["doc_type"]
    extractor = _EXTRACTORS.get(doc_type, _extract_txt)
    raw_text = extractor(doc["raw_bytes"])
    full_text = _clean_text(raw_text)

    metadata = {k: v for k, v in doc.items() if k != "raw_bytes"}

    return {
        "doc_id": doc["doc_id"],
        "full_text": full_text,
        "metadata": metadata,
    }
