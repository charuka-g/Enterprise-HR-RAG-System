import { useState, useEffect } from "react";
import type { UserProfile } from "../types";
import ChatWindow from "./ChatWindow";

type Mode = "closed" | "panel" | "fullscreen";

interface Props {
  user: UserProfile;
}

export default function ChatBubble({ user }: Props) {
  const [mode, setMode] = useState<Mode>("closed");
  const [showHint, setShowHint] = useState(false);

  // Show hint shortly after mount, auto-dismiss after 6 s
  useEffect(() => {
    const show = setTimeout(() => setShowHint(true), 800);
    const hide = setTimeout(() => setShowHint(false), 7000);
    return () => { clearTimeout(show); clearTimeout(hide); };
  }, []);

  const open = () => { setShowHint(false); setMode("panel"); };
  const close = () => setMode("closed");
  const toggleFullscreen = () =>
    setMode((m) => (m === "fullscreen" ? "panel" : "fullscreen"));

  return (
    <>
      {/* ── Floating Action Button (closed state) ── */}
      {mode === "closed" && (
        <>
          {/* Hint callout */}
          {showHint && (
            <div className="fixed bottom-24 right-6 z-40 flex flex-col items-end gap-1 animate-fade-in">
              <div className="bg-slate-900 text-white text-sm rounded-xl px-4 py-3 shadow-xl max-w-[220px] relative">
                <button
                  onClick={() => setShowHint(false)}
                  className="absolute top-1.5 right-2 text-slate-400 hover:text-white text-xs leading-none"
                  aria-label="Dismiss"
                >
                  ✕
                </button>
                <p className="font-semibold mb-0.5 pr-4">Meet myHR Assistant ✨</p>
                <p className="text-slate-300 text-xs leading-snug">
                  Get instant AI-powered answers to any HR policy question.
                </p>
              </div>
              {/* Arrow pointing down toward the FAB */}
              <svg width="20" height="12" viewBox="0 0 20 12" className="mr-5 text-slate-900" fill="currentColor">
                <path d="M10 12 L0 0 L20 0 Z" />
              </svg>
            </div>
          )}

        <button
          onClick={open}
          aria-label="Open HR Assistant"
          className="fixed bottom-6 right-6 z-40 w-14 h-14 bg-blue-600 hover:bg-blue-700 active:scale-95 text-white rounded-full shadow-xl flex items-center justify-center transition-all"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </button>
        </>
      )}

      {/* ── Panel (bottom-right bubble) ── */}
      {mode === "panel" && (
        <div className="fixed bottom-6 right-6 z-40 w-[380px] h-[580px] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-200">
          <ChatWindow
            user={user}
            onClose={close}
            onToggleFullscreen={toggleFullscreen}
            isFullscreen={false}
          />
        </div>
      )}

      {/* ── Fullscreen overlay ── */}
      {mode === "fullscreen" && (
        <div className="fixed inset-0 z-50 bg-white flex flex-col">
          <ChatWindow
            user={user}
            onClose={close}
            onToggleFullscreen={toggleFullscreen}
            isFullscreen={true}
          />
        </div>
      )}
    </>
  );
}
