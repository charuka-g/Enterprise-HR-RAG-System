#!/usr/bin/env python3
"""Entry point: runs the full ingestion pipeline."""
import argparse
import sys
import os
from dotenv import load_dotenv

load_dotenv()

from config import DOCS_DIR
from ingestion.loader import discover_docs
from ingestion.extractor import extract_text
from ingestion.chunker import chunk_document
from ingestion.embedder import embed_batch
from ingestion.indexer import ensure_table, index_chunks


def main(reset: bool = False) -> None:
    print("=== myHR Ingestion Pipeline ===\n")

    # 1. Discover docs
    print(f"Discovering documents in '{DOCS_DIR}'...")
    docs = discover_docs(DOCS_DIR)
    if not docs:
        print("No documents found. Drop files into the docs/ folder and re-run.")
        sys.exit(0)
    print(f"Found {len(docs)} document(s)\n")

    # 2. Extract text
    print("Extracting text...")
    extracted = []
    for doc in docs:
        try:
            result = extract_text(doc)
            if result["full_text"].strip():
                extracted.append(result)
                print(f"  [OK] {doc['file_name']} — {len(result['full_text'])} chars")
            else:
                print(f"  [SKIP] {doc['file_name']} — no text extracted")
        except Exception as e:
            print(f"  [ERROR] {doc['file_name']}: {e}")

    print(f"\nExtracted text from {len(extracted)}/{len(docs)} document(s)\n")

    # 3. Chunk
    print("Chunking documents...")
    all_chunks = []
    for doc in extracted:
        chunks = chunk_document(doc)
        print(f"  {doc['metadata']['file_name']}: {len(chunks)} chunk(s)")
        all_chunks.extend(chunks)
    print(f"\nTotal chunks: {len(all_chunks)}\n")

    if not all_chunks:
        print("No chunks to index. Exiting.")
        sys.exit(0)

    # 4. Embed
    print("Generating embeddings...")
    texts = [c["chunk_text"] for c in all_chunks]
    embeddings = embed_batch(texts)
    print(f"Generated {len(embeddings)} embeddings\n")

    # 5. Index
    print("Setting up PostgreSQL table...")
    ensure_table(reset=reset)

    print("\nIndexing chunks into PostgreSQL...")
    indexed = index_chunks(all_chunks, embeddings)

    print(f"\n=== Done ===")
    print(f"Processed: {len(extracted)} document(s)")
    print(f"Indexed:   {indexed} chunk(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="myHR ingestion pipeline")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate the PostgreSQL table before indexing",
    )
    args = parser.parse_args()
    main(reset=args.reset)
