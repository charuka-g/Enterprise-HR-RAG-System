from fastapi import APIRouter, HTTPException
from app.models import FeedbackRequest
from app.logger import update_feedback

router = APIRouter()


@router.post("/feedback")
def feedback(request: FeedbackRequest) -> dict:
    updated = update_feedback(
        query_id=request.query_id,
        rating=request.rating,
        comment=request.comment,
    )
    if not updated:
        raise HTTPException(status_code=404, detail=f"query_id '{request.query_id}' not found")
    return {"status": "ok"}
