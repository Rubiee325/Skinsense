import React from "react";
import { Routes, Route, NavLink } from "react-router-dom";
import Onboarding from "./pages/Onboarding";
import Capture from "./pages/Capture";
import Result from "./pages/Result";
import Timeline from "./pages/Timeline";
import Simulator from "./pages/Simulator";
import Recommendations from "./pages/Recommendations";
import Referral from "./pages/Referral";

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="px-4 py-3 border-b border-slate-800 flex items-center justify-between bg-slate-950/70 backdrop-blur">
        <span className="font-semibold text-lg tracking-tight">
          SkinMorph
        </span>
        <nav className="flex gap-3 text-xs sm:text-sm">
          <NavLink to="/" className="hover:text-teal-300">
            Onboard
          </NavLink>
          <NavLink to="/capture" className="hover:text-teal-300">
            Capture
          </NavLink>
          <NavLink to="/timeline" className="hover:text-teal-300">
            Timeline
          </NavLink>
        </nav>
      </header>
      <main className="flex-1 px-4 py-4 max-w-3xl mx-auto w-full">
        <Routes>
          <Route path="/" element={<Onboarding />} />
          <Route path="/capture" element={<Capture />} />
          <Route path="/result" element={<Result />} />
          <Route path="/timeline" element={<Timeline />} />
          <Route path="/simulator" element={<Simulator />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/referral" element={<Referral />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;






