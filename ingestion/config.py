import os
from dotenv import load_dotenv

load_dotenv()

DOCS_DIR = "docs"
SUPABASE_DB_URL = os.environ["SUPABASE_DB_URL"]  # required — PostgreSQL connection string
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]    # required
EMBEDDING_MODEL = "text-embedding-3-small"        # 1536-dim, fast & cheap
EMBEDDING_DIM = 1536
CHUNK_SIZE_TOKENS = 250      # target tokens per chunk
CHUNK_OVERLAP_TOKENS = 50    # overlap between consecutive chunks
BATCH_SIZE = 64              # how many chunks to upsert per batch
