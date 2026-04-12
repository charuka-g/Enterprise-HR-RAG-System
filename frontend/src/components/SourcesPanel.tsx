import { useState } from "react";
import type { SourceChunk } from "../types";

interface Props {
  sources: SourceChunk[];
}

function SourceCard({ source }: { source: SourceChunk }) {
  const [expanded, setExpanded] = useState(false);
  const preview = source.chunkText.slice(0, 200);
  const hasMore = source.chunkText.length > 200;

  return (
    <div className="border border-gray-200 rounded-lg p-3 text-sm bg-gray-50">
      <div className="flex items-center justify-between mb-1">
        <span className="font-semibold text-gray-800 truncate max-w-[70%]">
          {source.fileName}
        </span>
        <span className="text-xs text-green-600 font-medium">
          {Math.round(source.score * 100)}% match
        </span>
      </div>
      <p className="text-gray-600 text-xs leading-relaxed">
        {expanded ? source.chunkText : preview}
        {!expanded && hasMore && "..."}
      </p>
      {hasMore && (
        <button
          onClick={() => setExpanded((v) => !v)}
          className="text-xs text-blue-500 hover:underline mt-1"
        >
          {expanded ? "Show less" : "Show more"}
        </button>
      )}
    </div>
  );
}

export default function SourcesPanel({ sources }: Props) {
  const [open, setOpen] = useState(false);

  if (!sources.length) return null;

  return (
    <div className="mt-2">
      <button
        onClick={() => setOpen((v) => !v)}
        className="text-xs text-blue-500 hover:underline flex items-center gap-1"
      >
        <span>{open ? "v" : ">"}</span>
        View sources ({sources.length})
      </button>
      {open && (
        <div className="mt-2 space-y-2">
          {sources.map((s) => (
            <SourceCard key={s.chunkId} source={s} />
          ))}
        </div>
      )}
    </div>
  );
}
