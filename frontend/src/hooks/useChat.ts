import { useState, useCallback } from "react";
import type { Message, UserProfile } from "../types";
import { sendQuery, sendFeedback } from "../api";

function generateId(): string {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export function useChat(user: UserProfile) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(
    async (text: string) => {
      const userMessage: Message = {
        id: generateId(),
        role: "user",
        content: text,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const response = await sendQuery(text, user);

        const assistantMessage: Message = {
          id: generateId(),
          role: "assistant",
          content: response.answer,
          sources: response.sources,
          queryId: response.queryId,
          rating: null,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        const errorMessage: Message = {
          id: generateId(),
          role: "assistant",
          content: "Something went wrong, please try again.",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [user]
  );

  const submitFeedback = useCallback(
    async (queryId: string, rating: 1 | -1, comment = "") => {
      try {
        await sendFeedback(queryId, rating, comment);
        setMessages((prev) =>
          prev.map((msg) =>
            msg.queryId === queryId ? { ...msg, rating } : msg
          )
        );
      } catch {
        // Feedback failures are non-critical; silently ignore
      }
    },
    []
  );

  return { messages, isLoading, sendMessage, submitFeedback };
}
