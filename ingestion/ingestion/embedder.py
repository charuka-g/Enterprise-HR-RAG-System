import math
from tqdm import tqdm
import openai

from config import OPENAI_API_KEY, EMBEDDING_MODEL, BATCH_SIZE

_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts, splitting into batches of BATCH_SIZE."""
    all_embeddings = []
    n_batches = math.ceil(len(texts) / BATCH_SIZE)

    for batch_idx in tqdm(range(n_batches), desc="Embedding batches"):
        batch = texts[batch_idx * BATCH_SIZE : (batch_idx + 1) * BATCH_SIZE]
        response = _client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        all_embeddings.extend([item.embedding for item in response.data])

    return all_embeddings
