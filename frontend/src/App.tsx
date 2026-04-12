import { useState } from "react";
import type { UserProfile } from "./types";
import LoginScreen from "./components/LoginScreen";
import PortalLayout from "./components/PortalLayout";

export default function App() {
  const [user, setUser] = useState<UserProfile | null>(null);

  if (!user) {
    return <LoginScreen onLogin={setUser} />;
  }

  return <PortalLayout user={user} onSignOut={() => setUser(null)} />;
}
