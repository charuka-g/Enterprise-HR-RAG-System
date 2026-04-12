from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.query import router as query_router
from app.routes.feedback import router as feedback_router

app = FastAPI(title="myHR API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router, prefix="/api")
app.include_router(feedback_router, prefix="/api")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
