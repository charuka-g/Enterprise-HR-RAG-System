from pydantic import BaseModel


class QueryRequest(BaseModel):
    user_question: str
    user_id: str = "anonymous"
    business_unit: str = "all"       # used for metadata filter
    country: str = "global"          # used for metadata filter
    acl_groups: list[str] = ["all"]  # used for ACL filter


class SourceChunk(BaseModel):
    chunk_id: str
    doc_id: str
    file_name: str
    chunk_text: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    query_id: str                    # UUID for this query (used for feedback)
    retrieval_latency_ms: float
    generation_latency_ms: float
    total_latency_ms: float


class FeedbackRequest(BaseModel):
    query_id: str
    rating: int                      # 1 = thumbs up, -1 = thumbs down
    comment: str = ""
