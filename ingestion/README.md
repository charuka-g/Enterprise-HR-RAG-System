# myHR — Ingestion Pipeline

Standalone Python pipeline that reads HR documents, extracts text, chunks it, generates embeddings, and indexes everything into Qdrant.

## Prerequisites

- Docker Desktop (for Qdrant)
- Python 3.10+
- An OpenAI API key

## 1. Start Qdrant

```bash
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

Or from the project root:

```bash
docker compose up -d
```

## 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Add HR documents

Drop files into the `docs/` folder. Supported formats: PDF, DOCX, DOC, HTML, HTM, TXT.

### Folder naming convention for metadata extraction

The pipeline infers `business_unit`, `country`, and `acl_groups` from the folder structure:

| Folder path | business_unit | country | acl_groups |
|---|---|---|---|
| `docs/BU_Finance/LK/file.pdf` | Finance | LK | ["Finance"] |
| `docs/BU_HR/SG/file.docx` | HR | SG | ["HR"] |
| `docs/global/policy.pdf` | global | global | ["all"] |
| `docs/file.pdf` (root) | general | global | ["all"] |

## 5. Run the pipeline

```bash
python main.py
```

## 6. Reset and re-index

To drop the existing Qdrant collection and re-index everything from scratch:

```bash
python main.py --reset
```
