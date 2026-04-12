import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector

from app.config import settings

TABLE_NAME = "hr_chunks"

import os
from dotenv import load_dotenv

load_dotenv()


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


def retrieve(
    query_embedding: list[float],
    business_unit: str = "all",
    country: str = "global",
    acl_groups: list[str] = None,
    top_k: int = None,
) -> list[dict]:
    """Search PostgreSQL for the top_k most relevant chunks with optional metadata filters."""
    if acl_groups is None:
        acl_groups = ["all"]
    if top_k is None:
        top_k = settings.top_k_retrieve

    embedding_vec = np.array(query_embedding)

    where_clauses = []
    params: list = [embedding_vec]  # first %s is for the SELECT score calculation

    if business_unit != "all":
        where_clauses.append("(business_unit = %s OR business_unit IN ('global', 'general'))")
        params.append(business_unit)

    if country != "global":
        where_clauses.append("(country = %s OR country = 'global')")
        params.append(country)

    # ACL filter — skip if user has ["all"] (admin/open access)
    if acl_groups != ["all"]:
        where_clauses.append("(acl_groups && %s)")
        params.append(acl_groups + ["all"])

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    # embedding_vec appears twice: once in SELECT for score, once in ORDER BY
    params.extend([embedding_vec, top_k])

    query = f"""
        SELECT
            chunk_id, doc_id, chunk_index, chunk_text, token_count,
            file_path, file_name, doc_type, business_unit, country,
            acl_groups, last_updated,
            1 - (embedding <=> %s) AS score
        FROM {TABLE_NAME}
        {where_sql}
        ORDER BY embedding <=> %s
        LIMIT %s
    """

    conn = _get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
    finally:
        conn.close()

    return [dict(row) for row in rows]
