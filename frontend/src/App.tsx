import { useState } from "react";
import type { UserProfile } from "./types";
import LoginScreen from "./components/LoginScreen";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  const [user, setUser] = useState<UserProfile | null>(null);

  if (!user) {
    return <LoginScreen onLogin={setUser} />;
  }

  return <ChatWindow user={user} onSignOut={() => setUser(null)} />;
}
