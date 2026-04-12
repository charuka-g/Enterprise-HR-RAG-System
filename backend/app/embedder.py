import openai
from app.config import settings

_client = openai.OpenAI(api_key=settings.openai_api_key)


def embed_query(text: str) -> list[float]:
    """Embed a single query string using text-embedding-3-small."""
    response = _client.embeddings.create(
        model=settings.embedding_model,
        input=[text],
    )
    return response.data[0].embedding
