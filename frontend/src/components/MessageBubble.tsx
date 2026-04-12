import ReactMarkdown from "react-markdown";
import type { Message } from "../types";
import SourcesPanel from "./SourcesPanel";
import FeedbackButtons from "./FeedbackButtons";

interface Props {
  message: Message;
  onFeedback: (queryId: string, rating: 1 | -1, comment: string) => void;
}

export default function MessageBubble({ message, onFeedback }: Props) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end mb-4">
        <div className="bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-2 max-w-[80%] text-sm">
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-3 mb-4">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-xs font-bold text-blue-700">
        HR
      </div>
      <div className="flex-1 max-w-[85%]">
        <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 text-sm text-gray-800 shadow-sm">
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              ul: ({ children }) => (
                <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>
              ),
              li: ({ children }) => <li className="ml-2">{children}</li>,
              strong: ({ children }) => (
                <strong className="font-semibold">{children}</strong>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {message.sources && message.sources.length > 0 && (
          <SourcesPanel sources={message.sources} />
        )}

        {message.queryId && (
          <FeedbackButtons
            queryId={message.queryId}
            rating={message.rating}
            onFeedback={onFeedback}
          />
        )}
      </div>
    </div>
  );
}
