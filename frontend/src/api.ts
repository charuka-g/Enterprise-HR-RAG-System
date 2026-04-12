import type { UserProfile, QueryResponse } from "./types";

// In dev, VITE_API_BASE_URL is empty and Vite proxies /api/* to localhost:8000.
// In prod, set VITE_API_BASE_URL to the deployed backend origin (e.g. https://api.myhr.com).
const BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

export async function sendQuery(
  question: string,
  user: UserProfile
): Promise<QueryResponse> {
  const res = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_question: question,
      user_id: user.userId,
      business_unit: user.businessUnit,
      country: user.country,
      acl_groups: user.aclGroups,
    }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail ?? `HTTP ${res.status}`);
  }

  const data = await res.json();

  // Map snake_case response to camelCase
  return {
    answer: data.answer,
    sources: (data.sources ?? []).map((s: Record<string, unknown>) => ({
      chunkId: s.chunk_id,
      docId: s.doc_id,
      fileName: s.file_name,
      chunkText: s.chunk_text,
      score: s.score,
    })),
    queryId: data.query_id,
    retrievalLatencyMs: data.retrieval_latency_ms,
    generationLatencyMs: data.generation_latency_ms,
    totalLatencyMs: data.total_latency_ms,
  };
}

export async function sendFeedback(
  queryId: string,
  rating: 1 | -1,
  comment = ""
): Promise<void> {
  const res = await fetch(`${BASE_URL}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query_id: queryId, rating, comment }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail ?? `HTTP ${res.status}`);
  }
}
