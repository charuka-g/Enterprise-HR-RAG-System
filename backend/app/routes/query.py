import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from app.models import QueryRequest, QueryResponse, SourceChunk
from app.embedder import embed_query
from app.retriever import retrieve
from app.generator import generate
from app.logger import log_query
from app.config import settings

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    query_id = str(uuid.uuid4())
    total_start = time.perf_counter()

    # 1. Embed query
    retrieval_start = time.perf_counter()
    try:
        query_embedding = embed_query(request.user_question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Embedding error: {e}")

    # 2. Retrieve from Qdrant
    try:
        all_chunks = retrieve(
            query_embedding=query_embedding,
            business_unit=request.business_unit,
            country=request.country,
            acl_groups=request.acl_groups,
            top_k=settings.top_k_retrieve,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Retrieval error: {e}")

    retrieval_latency_ms = (time.perf_counter() - retrieval_start) * 1000

    # 3. Select top_k_prompt chunks
    top_chunks = all_chunks[: settings.top_k_prompt]

    # 4. Generate answer
    generation_start = time.perf_counter()
    try:
        answer = generate(request.user_question, top_chunks)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Generation error: {e}")
    generation_latency_ms = (time.perf_counter() - generation_start) * 1000

    total_latency_ms = (time.perf_counter() - total_start) * 1000

    # 5. Build source list
    sources = [
        SourceChunk(
            chunk_id=c.get("chunk_id", ""),
            doc_id=c.get("doc_id", ""),
            file_name=c.get("file_name", ""),
            chunk_text=c.get("chunk_text", ""),
            score=c.get("score", 0.0),
        )
        for c in top_chunks
    ]

    # 6. Log
    log_query({
        "query_id": query_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": request.user_id,
        "user_question": request.user_question,
        "business_unit": request.business_unit,
        "country": request.country,
        "chunk_ids_used": [c.get("chunk_id", "") for c in top_chunks],
        "top_scores": [c.get("score", 0.0) for c in top_chunks],
        "retrieval_latency_ms": round(retrieval_latency_ms, 2),
        "generation_latency_ms": round(generation_latency_ms, 2),
        "total_latency_ms": round(total_latency_ms, 2),
        "rating": None,
        "comment": "",
    })

    return QueryResponse(
        answer=answer,
        sources=sources,
        query_id=query_id,
        retrieval_latency_ms=round(retrieval_latency_ms, 2),
        generation_latency_ms=round(generation_latency_ms, 2),
        total_latency_ms=round(total_latency_ms, 2),
    )
