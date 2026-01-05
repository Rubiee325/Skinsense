import React from "react";
import { useLocation } from "react-router-dom";

const Recommendations: React.FC = () => {
  const location = useLocation();
  const recs = (location.state as any)?.result?.recommendations ?? [];

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Recommendations</h2>
      <p className="text-sm text-slate-300">
        Evidence-inspired, rule-based suggestions derived from model outputs.
        Always validate with a clinician.
      </p>
      <ul className="space-y-2">
        {recs.map((r: any, idx: number) => (
          <li
            key={idx}
            className="border border-slate-800 rounded-lg p-3 text-sm"
          >
            <div className="font-semibold">{r.title}</div>
            <div className="text-slate-300">{r.summary}</div>
            <div className="mt-1 text-xs text-slate-400">
              Evidence: {r.evidence_level}
            </div>
            <div className="mt-1 text-xs text-amber-300">
              {r.when_to_see_doctor}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Recommendations;






