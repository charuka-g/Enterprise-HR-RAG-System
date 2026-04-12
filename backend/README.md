# myHR — Backend API

FastAPI server that handles employee HR queries via RAG: embeds questions, retrieves relevant chunks from Qdrant, and generates answers with GPT-4o.

## Prerequisites

- Python 3.10+
- Qdrant running locally (see root README)
- Ingestion pipeline has been run (see `ingestion/`)

## 1. Configure environment

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

## 4. API documentation

Interactive docs: http://localhost:8000/docs

## Example: POST /api/query

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_question": "How many days of annual leave do I get?",
    "user_id": "alice",
    "business_unit": "Finance",
    "country": "LK",
    "acl_groups": ["Finance"]
  }'
```

## Example: POST /api/feedback

```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "query_id": "<query_id from response>",
    "rating": 1,
    "comment": "Very helpful!"
  }'
```

## Health check

```bash
curl http://localhost:8000/health
```
