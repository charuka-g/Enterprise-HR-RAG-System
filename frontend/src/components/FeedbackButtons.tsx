import { useState } from "react";

interface Props {
  queryId: string;
  rating?: 1 | -1 | null;
  onFeedback: (queryId: string, rating: 1 | -1, comment: string) => void;
}

export default function FeedbackButtons({ queryId, rating, onFeedback }: Props) {
  const [showComment, setShowComment] = useState(false);
  const [comment, setComment] = useState("");

  const hasRated = rating !== null && rating !== undefined;

  function handleThumbsUp() {
    if (hasRated) return;
    onFeedback(queryId, 1, "");
  }

  function handleThumbsDown() {
    if (hasRated) return;
    setShowComment(true);
  }

  function handleCommentSubmit() {
    onFeedback(queryId, -1, comment);
    setShowComment(false);
  }

  return (
    <div className="mt-2">
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-400">Was this helpful?</span>
        <button
          onClick={handleThumbsUp}
          disabled={hasRated}
          className={`text-lg transition-opacity ${
            hasRated
              ? rating === 1
                ? "opacity-100"
                : "opacity-30"
              : "hover:scale-110 cursor-pointer"
          }`}
          title="Helpful"
        >
          +1
        </button>
        <button
          onClick={handleThumbsDown}
          disabled={hasRated}
          className={`text-lg transition-opacity ${
            hasRated
              ? rating === -1
                ? "opacity-100"
                : "opacity-30"
              : "hover:scale-110 cursor-pointer"
          }`}
          title="Not helpful"
        >
          -1
        </button>
      </div>

      {showComment && !hasRated && (
        <div className="mt-2 flex gap-2 items-start">
          <input
            type="text"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="What could be better? (optional)"
            className="flex-1 border border-gray-300 rounded px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-blue-400"
            onKeyDown={(e) => e.key === "Enter" && handleCommentSubmit()}
          />
          <button
            onClick={handleCommentSubmit}
            className="text-xs bg-gray-200 hover:bg-gray-300 rounded px-2 py-1"
          >
            Submit
          </button>
        </div>
      )}
    </div>
  );
}
