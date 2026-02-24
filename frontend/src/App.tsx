import React, { useState, useEffect } from "react";
import { Routes, Route, NavLink, useNavigate, Navigate } from "react-router-dom";
import Onboarding from "./pages/Onboarding";
import Capture from "./pages/Capture";
import Result from "./pages/Result";
import Timeline from "./pages/Timeline";
import Simulator from "./pages/Simulator";
import Recommendations from "./pages/Recommendations";
import Referral from "./pages/Referral";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import DermatologistDashboard from "./pages/DermatologistDashboard";
import { logout } from "./api";

const App: React.FC = () => {
  const [user, setUser] = useState<any>(null);
  const [role, setRole] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("skinmorph_user");
    const storedRole = localStorage.getItem("skinmorph_role");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setRole(storedRole);
    }
  }, []);

  const handleLogout = () => {
    logout();
    setUser(null);
    setRole(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-200">
      <header className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/70 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-teal-500 rounded-lg flex items-center justify-center">
            <span className="text-slate-950 font-black text-xl">S</span>
          </div>
          <span className="font-bold text-xl tracking-tight text-white">
            SkinMorph
          </span>
        </div>

        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          {role === "patient" && (
            <>
              <NavLink to="/" className={({ isActive }) => isActive ? "text-teal-400" : "text-slate-400 hover:text-white transition-colors"}>
                Dashboard
              </NavLink>
              <NavLink to="/capture" className={({ isActive }) => isActive ? "text-teal-400" : "text-slate-400 hover:text-white transition-colors"}>
                Analyze
              </NavLink>
              <NavLink to="/timeline" className={({ isActive }) => isActive ? "text-teal-400" : "text-slate-400 hover:text-white transition-colors"}>
                History
              </NavLink>
            </>
          )}
          {role === "dermatologist" && (
            <NavLink to="/dermatologist/dashboard" className={({ isActive }) => isActive ? "text-teal-400" : "text-slate-400 hover:text-white transition-colors"}>
              Clinician Panel
            </NavLink>
          )}
        </nav>

        <div className="flex items-center gap-4">
          {user ? (
            <div className="flex items-center gap-3 pl-4 border-l border-slate-800">
              <div className="text-right hidden sm:block">
                <p className="text-xs font-bold text-white uppercase">{user.name}</p>
                <p className="text-[10px] text-teal-500 font-bold uppercase tracking-wider">{role}</p>
              </div>
              <button
                onClick={handleLogout}
                className="p-2 text-slate-400 hover:text-red-400 transition-colors"
                title="Sign out"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          ) : (
            <div className="flex gap-3">
              <NavLink to="/login" className="px-4 py-1.5 rounded-lg text-sm font-semibold hover:text-teal-400 transition-colors">
                Sign in
              </NavLink>
              <NavLink to="/signup" className="px-4 py-1.5 rounded-lg bg-teal-500 text-slate-950 text-sm font-bold hover:bg-teal-400 transition-all">
                Get Started
              </NavLink>
            </div>
          )}
        </div>
      </header>

      <main className="flex-1 px-4 py-8 max-w-5xl mx-auto w-full">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* Protected Routes */}
          <Route
            path="/"
            element={role === "dermatologist" ? <Navigate to="/dermatologist/dashboard" /> : <Onboarding />}
          />
          <Route path="/capture" element={<Capture />} />
          <Route path="/result" element={<Result />} />
          <Route path="/timeline" element={<Timeline />} />
          <Route path="/simulator" element={<Simulator />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/referral" element={<Referral />} />

          {/* Dermatologist specific */}
          <Route path="/dermatologist/dashboard" element={<DermatologistDashboard />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;






