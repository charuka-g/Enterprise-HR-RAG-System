import openai
from app.config import settings

_client = openai.OpenAI(api_key=settings.openai_api_key)

_SYSTEM_PROMPT = """You are myHR, an internal HR assistant. Answer employee questions using ONLY the provided HR policy context below.
- Give thorough, well-structured answers. Cover all relevant details, exceptions, and procedures found in the context.
- Organise your response with clear headings and bullet points where appropriate.
- Explain the "why" behind policies where the context supports it, not just the rules themselves.
- Include relevant eligibility criteria, timelines, responsibilities, and any special cases mentioned in the context.
- If the answer is not clearly supported by the context, say "I don't have enough information on this. Please contact HR directly."
- Do not make up policies or numbers."""


def generate(user_question: str, chunks: list[dict]) -> str:
    """Build a RAG prompt from chunks and call GPT to generate an answer."""
    if not chunks:
        return "No HR documents have been indexed yet. Please run the ingestion pipeline first."

    # Build numbered context block
    context_parts = []
    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(f"[{i}] Source: {chunk.get('file_name', 'unknown')}\n{chunk.get('chunk_text', '')}")
    context = "\n\n".join(context_parts)

    user_message = f"Context:\n{context}\n\nQuestion: {user_question}"

    response = _client.chat.completions.create(
        model=settings.openai_model,
        max_tokens=settings.max_tokens,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
