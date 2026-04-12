# myHR — Internal HR Chatbot

An internal HR chatbot powered by a RAG (Retrieval-Augmented Generation) pipeline. Employees ask natural-language HR questions and get instant, grounded answers sourced from HR policy documents.

## Architecture

| Service | Description |
|---|---|
| [ingestion/](ingestion/) | Reads HR docs, chunks them, generates embeddings, indexes into Qdrant |
| [backend/](backend/) | FastAPI RAG server — retrieves relevant chunks and generates answers with GPT-4o |
| [frontend/](frontend/) | React + Vite chat UI |

## Quickstart

### 1. Start Qdrant

```bash
docker compose up -d
```

Qdrant REST API: http://localhost:6333

### 2. Add HR documents

Drop PDF, DOCX, HTML, or TXT files into `ingestion/docs/`. Use subfolders to set metadata:

```
ingestion/docs/
  BU_Finance/LK/leave-policy.pdf
  BU_HR/SG/benefits.docx
  global/code-of-conduct.pdf
```

### 3. Run ingestion

```bash
cd ingestion
cp .env.example .env        # add your OPENAI_API_KEY
pip install -r requirements.txt
python main.py
```

To reset and re-index: `python main.py --reset`

### 4. Start backend

```bash
cd backend
cp .env.example .env        # add your OPENAI_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 5. Start frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Requirements

- Docker Desktop
- Python 3.10+
- Node.js 18+
- OpenAI API key
