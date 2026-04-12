import { useState } from "react";
import type { UserProfile } from "../types";

interface Props {
  onLogin: (profile: UserProfile) => void;
}

const BUSINESS_UNITS = ["Finance", "HR", "IT", "Operations", "General"];
const COUNTRIES = ["LK", "SG", "AU", "global"];

export default function LoginScreen({ onLogin }: Props) {
  const [name, setName] = useState("");
  const [businessUnit, setBusinessUnit] = useState("General");
  const [country, setCountry] = useState("global");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;

    const aclGroups =
      businessUnit === "General" ? ["all"] : [businessUnit];

    onLogin({
      userId: name.trim(),
      businessUnit: businessUnit === "General" ? "all" : businessUnit,
      country,
      aclGroups,
    });
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-blue-100 mb-4">
            <span className="text-2xl">HR</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">myHR Assistant</h1>
          <p className="text-sm text-gray-500 mt-1">
            Your internal HR knowledge companion
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Employee Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Business Unit
            </label>
            <select
              value={businessUnit}
              onChange={(e) => setBusinessUnit(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {BUSINESS_UNITS.map((bu) => (
                <option key={bu} value={bu}>
                  {bu}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Country
            </label>
            <select
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {COUNTRIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg text-sm transition-colors"
          >
            Start Chatting
          </button>
        </form>

        <p className="text-xs text-gray-400 text-center mt-6">
          Local development mode — no authentication required
        </p>
      </div>
    </div>
  );
}
