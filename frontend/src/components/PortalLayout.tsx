import type { UserProfile } from "../types";
import ChatBubble from "./ChatBubble";

interface Props {
  user: UserProfile;
  onSignOut: () => void;
}

const NAV_LINKS = ["Dashboard", "My Leave", "Benefits", "Payroll", "Directory", "Training"];

const ANNOUNCEMENTS = [
  {
    id: 1,
    date: "Apr 10, 2026",
    title: "Q2 Performance Reviews Now Open",
    body: "All managers are reminded to submit Q2 performance reviews by 30 April 2026 via the ESS portal.",
  },
  {
    id: 2,
    date: "Apr 7, 2026",
    title: "Remote Work Policy Updated",
    body: "The remote work policy has been revised effective 1 May 2026. Key changes include updated eligibility criteria and the Remote Work Allowance amount.",
  },
  {
    id: 3,
    date: "Mar 28, 2026",
    title: "Public Holiday – 14 April 2026",
    body: "Sinhala & Tamil New Year (14 April) is a gazetted public holiday. Please plan project timelines and client commitments accordingly.",
  },
  {
    id: 4,
    date: "Mar 20, 2026",
    title: "New Training Catalogue Available",
    body: "The Q2 training calendar is now live. Employees can browse and self-enrol in courses through the Learning & Development portal.",
  },
];

const QUICK_LINKS = [
  { label: "Apply for Leave", icon: "🗓️" },
  { label: "View Payslip", icon: "💳" },
  { label: "Submit Expense", icon: "🧾" },
  { label: "Book Training", icon: "📚" },
  { label: "IT Helpdesk", icon: "🖥️" },
  { label: "HR Contacts", icon: "📞" },
];

const HR_TEAM = [
  { name: "Priya Nair", role: "HR Business Partner – Finance & IT", email: "p.nair@meridian.lk" },
  { name: "Kasun Silva", role: "HR Business Partner – Operations", email: "k.silva@meridian.lk" },
  { name: "Amara Perera", role: "Payroll & Benefits Manager", email: "a.perera@meridian.lk" },
];

export default function PortalLayout({ user, onSignOut }: Props) {
  const firstName = user.userId.split(" ")[0];
  const today = new Date().toLocaleDateString("en-GB", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* ── Top Navigation ── */}
      <nav className="bg-slate-900 text-white flex items-center justify-between px-6 h-14 shadow-lg flex-shrink-0">
        {/* Logo + Nav Links */}
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2.5 flex-shrink-0">
            <div className="w-7 h-7 rounded bg-blue-500 flex items-center justify-center font-bold text-sm">
              M
            </div>
            <span className="font-semibold text-sm tracking-wide whitespace-nowrap">
              Meridian Holdings
            </span>
          </div>
          <div className="hidden md:flex items-center">
            {NAV_LINKS.map((link) => (
              <button
                key={link}
                className={`px-3 h-14 text-sm transition-colors hover:bg-slate-700 ${
                  link === "Dashboard"
                    ? "border-b-2 border-blue-400 text-white"
                    : "text-slate-300 hover:text-white"
                }`}
              >
                {link}
              </button>
            ))}
          </div>
        </div>

        {/* User Info + Sign Out */}
        <div className="flex items-center gap-3">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium leading-none">{user.userId}</p>
            <p className="text-xs text-slate-400 mt-0.5">
              {user.businessUnit} · {user.country.toUpperCase()}
            </p>
          </div>
          <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-sm font-bold uppercase flex-shrink-0">
            {user.userId[0]}
          </div>
          <button
            onClick={onSignOut}
            className="text-xs text-slate-400 hover:text-white border border-slate-600 hover:border-slate-400 rounded px-2 py-1 transition-colors"
          >
            Sign out
          </button>
        </div>
      </nav>

      {/* ── Main Content ── */}
      <main className="flex-1 px-4 sm:px-6 py-6 max-w-7xl mx-auto w-full">

        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-slate-800 to-blue-900 text-white rounded-xl px-6 py-5 mb-6 shadow-md">
          <p className="text-xs text-blue-300 mb-1">{today}</p>
          <h1 className="text-2xl font-bold">Good morning, {firstName} 👋</h1>
          <p className="text-sm text-blue-200 mt-1">
            Welcome to the Meridian Holdings employee portal.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">
              Annual Leave Balance
            </p>
            <p className="text-3xl font-bold text-gray-900">
              18{" "}
              <span className="text-base font-normal text-gray-400">days</span>
            </p>
            <p className="text-xs text-amber-500 mt-1">3 days pending approval</p>
          </div>

          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">
              Next Public Holiday
            </p>
            <p className="text-xl font-bold text-gray-900">14 April 2026</p>
            <p className="text-xs text-gray-400 mt-1">Sinhala &amp; Tamil New Year</p>
          </div>

          <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">
              Next Payslip
            </p>
            <p className="text-xl font-bold text-gray-900">30 April 2026</p>
            <p className="text-xs text-gray-400 mt-1">March 2026 payroll</p>
          </div>
        </div>

        {/* Two-column grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* Announcements */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-4">
              Announcements
            </h2>
            <div className="space-y-5">
              {ANNOUNCEMENTS.map((a) => (
                <div key={a.id} className="border-l-4 border-blue-500 pl-4">
                  <p className="text-xs text-gray-400 mb-0.5">{a.date}</p>
                  <p className="text-sm font-semibold text-gray-800">{a.title}</p>
                  <p className="text-sm text-gray-600 mt-0.5 leading-relaxed">{a.body}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right column */}
          <div className="flex flex-col gap-6">

            {/* Quick Links */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
              <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-4">
                Quick Links
              </h2>
              <div className="grid grid-cols-2 gap-2.5">
                {QUICK_LINKS.map((l) => (
                  <button
                    key={l.label}
                    className="flex flex-col items-center gap-1.5 p-3 rounded-lg border border-gray-100 hover:bg-blue-50 hover:border-blue-200 transition-colors text-center"
                  >
                    <span className="text-xl">{l.icon}</span>
                    <span className="text-xs font-medium text-gray-600 leading-tight">
                      {l.label}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* HR Team */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
              <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-4">
                Your HR Team
              </h2>
              <div className="space-y-3">
                {HR_TEAM.map((p) => (
                  <div key={p.name} className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-600 flex-shrink-0 mt-0.5">
                      {p.name[0]}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-800">{p.name}</p>
                      <p className="text-xs text-gray-400 leading-snug">{p.role}</p>
                      <a
                        href={`mailto:${p.email}`}
                        className="text-xs text-blue-500 hover:underline"
                      >
                        {p.email}
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* ── Chat Bubble ── */}
      <ChatBubble user={user} />
    </div>
  );
}
