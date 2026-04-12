export interface UserProfile {
  userId: string;
  businessUnit: string;
  country: string;
  aclGroups: string[];
}

export interface SourceChunk {
  chunkId: string;
  docId: string;
  fileName: string;
  chunkText: string;
  score: number;
}

export interface QueryResponse {
  answer: string;
  sources: SourceChunk[];
  queryId: string;
  retrievalLatencyMs: number;
  generationLatencyMs: number;
  totalLatencyMs: number;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: SourceChunk[];
  queryId?: string;
  rating?: 1 | -1 | null;
  timestamp: Date;
}
