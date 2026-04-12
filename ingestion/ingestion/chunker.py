import re
import tiktoken

from config import CHUNK_SIZE_TOKENS, CHUNK_OVERLAP_TOKENS

_ENCODING = tiktoken.get_encoding("cl100k_base")

def _token_count(text: str) -> int:
    return len(_ENCODING.encode(text))

def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_document(doc: dict) -> list[dict]:
    """Chunk a document's full_text into overlapping token windows."""
    full_text = doc["full_text"]
    doc_id = doc["doc_id"]
    metadata = doc["metadata"]

    sentences = _split_sentences(full_text)
    if not sentences:
        return []

    chunks = []
    chunk_index = 0
    i = 0

    while i < len(sentences):
        current_sentences = []
        current_tokens = 0

        j = i
        while j < len(sentences):
            sentence_tokens = _token_count(sentences[j])
            if current_tokens + sentence_tokens > CHUNK_SIZE_TOKENS and current_sentences:
                break
            current_sentences.append(sentences[j])
            current_tokens += sentence_tokens
            j += 1

        chunk_text = " ".join(current_sentences)
        token_count = _token_count(chunk_text)

        if token_count >= 30:
            chunk_id = f"{doc_id}_chunk_{chunk_index}"
            chunks.append({
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "chunk_index": chunk_index,
                "chunk_text": chunk_text,
                "token_count": token_count,
                "metadata": metadata,
            })
            chunk_index += 1

        # Back-track by CHUNK_OVERLAP_TOKENS worth of sentences
        overlap_tokens = 0
        back = j - 1
        while back >= i and overlap_tokens < CHUNK_OVERLAP_TOKENS:
            overlap_tokens += _token_count(sentences[back])
            back -= 1

        # Move i forward past i but keep overlap sentences
        new_i = max(i + 1, back + 2)
        if new_i <= i:
            new_i = i + 1
        i = new_i

    return chunks
