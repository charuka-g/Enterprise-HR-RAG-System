import numpy as np
import psycopg2
from psycopg2.extras import execute_batch
from pgvector.psycopg2 import register_vector
import os
from dotenv import load_dotenv

load_dotenv()

from config import SUPABASE_DB_URL, EMBEDDING_DIM, BATCH_SIZE

TABLE_NAME = "hr_chunks"


def _get_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRE_HOST"),
        dbname=os.getenv("POSTGRE_DB_NAME"),
        user=os.getenv("POSTGRE_DB_USER"),
        password=os.getenv("POSTGRE_PASSWORD"),
        port=int(os.getenv("POSTGRE_PORT", "5432")),
        sslmode="require",
    )
    register_vector(conn)
    return conn


def _chunk_id_to_int(chunk_id: str) -> int:
    return abs(hash(chunk_id)) % (2**63)


def ensure_table(reset: bool = False) -> None:
    """Create the hr_chunks table if it doesn't exist. If reset=True, drop and recreate."""
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            if reset:
                cur.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
                print(f"Dropped table '{TABLE_NAME}'")

            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id BIGINT PRIMARY KEY,
                    chunk_id TEXT NOT NULL UNIQUE,
                    doc_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    chunk_text TEXT NOT NULL,
                    token_count INTEGER NOT NULL,
                    file_path TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    doc_type TEXT NOT NULL,
                    business_unit TEXT NOT NULL,
                    country TEXT NOT NULL,
                    acl_groups TEXT[] NOT NULL,
                    last_updated TEXT NOT NULL,
                    embedding vector({EMBEDDING_DIM})
                );
            """)

            cur.execute(f"""
                CREATE INDEX IF NOT EXISTS {TABLE_NAME}_embedding_idx
                ON {TABLE_NAME} USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100);
            """)

        conn.commit()
        print(f"Table '{TABLE_NAME}' is ready")
    finally:
        conn.close()


def index_chunks(chunks: list[dict], embeddings: list[list[float]]) -> int:
    """Upsert chunks with their embeddings into PostgreSQL. Returns number of rows upserted."""
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            indexed = 0
            for i in range(0, len(chunks), BATCH_SIZE):
                batch_chunks = chunks[i : i + BATCH_SIZE]
                batch_embeddings = embeddings[i : i + BATCH_SIZE]

                rows = []
                for chunk, vector in zip(batch_chunks, batch_embeddings):
                    meta = chunk["metadata"]
                    rows.append((
                        _chunk_id_to_int(chunk["chunk_id"]),
                        chunk["chunk_id"],
                        chunk["doc_id"],
                        chunk["chunk_index"],
                        chunk["chunk_text"],
                        chunk["token_count"],
                        meta.get("file_path", ""),
                        meta.get("file_name", ""),
                        meta.get("doc_type", ""),
                        meta.get("business_unit", ""),
                        meta.get("country", ""),
                        meta.get("acl_groups", []),
                        meta.get("last_updated", ""),
                        np.array(vector),
                    ))

                execute_batch(
                    cur,
                    f"""
                    INSERT INTO {TABLE_NAME} (
                        id, chunk_id, doc_id, chunk_index, chunk_text, token_count,
                        file_path, file_name, doc_type, business_unit, country,
                        acl_groups, last_updated, embedding
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s
                    )
                    ON CONFLICT (chunk_id) DO UPDATE SET
                        doc_id = EXCLUDED.doc_id,
                        chunk_index = EXCLUDED.chunk_index,
                        chunk_text = EXCLUDED.chunk_text,
                        token_count = EXCLUDED.token_count,
                        file_path = EXCLUDED.file_path,
                        file_name = EXCLUDED.file_name,
                        doc_type = EXCLUDED.doc_type,
                        business_unit = EXCLUDED.business_unit,
                        country = EXCLUDED.country,
                        acl_groups = EXCLUDED.acl_groups,
                        last_updated = EXCLUDED.last_updated,
                        embedding = EXCLUDED.embedding
                    """,
                    rows,
                    page_size=BATCH_SIZE,
                )

                indexed += len(batch_chunks)
                print(f"  Indexed {indexed}/{len(chunks)} chunks...")
                conn.commit()
    finally:
        conn.close()

    return indexed
