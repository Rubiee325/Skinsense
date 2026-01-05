import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { predictSequence } from "../api";

interface LocationState {
  rawImage?: string | null;
}

const Simulator: React.FC = () => {
  const location = useLocation();
  const state = location.state as LocationState | null;
  const [loading, setLoading] = useState(false);
  const [risks, setRisks] = useState<any | null>(null);
  const [visuals, setVisuals] = useState<Record<string, string> | null>(null);

  const handleDemoSim = async () => {
    // This demo just calls predict_sequence with the same file multiple times.
    if (!state?.rawImage) return;
    setLoading(true);
    try {
      const resp = await fetch(state.rawImage);
      const blob = await resp.blob();
      const file = new File([blob], "frame.png", { type: blob.type });
      const data = await predictSequence([file, file, file]);
      setRisks(data.risks);
      setVisuals(data.future_visuals_png_b64 ?? null);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">SkinMorph simulator</h2>
      <p className="text-sm text-slate-300">
        Prototype simulation of future risk trajectories at 30 days, 6 months,
        and 1 year. Values are research-only and not clinically validated.
      </p>
      <button
        onClick={handleDemoSim}
        disabled={loading}
        className="inline-flex px-4 py-2 rounded-md bg-teal-500 text-slate-950 text-sm font-medium disabled:opacity-60"
      >
        {loading ? "Simulating..." : "Run demo simulation"}
      </button>
      {risks && (
        <div className="space-y-3">
          {Object.entries(risks).map(([tp, r]: any) => (
            <div
              key={tp}
              className="border border-slate-800 rounded-lg p-3 text-sm"
            >
              <div className="font-semibold mb-1">{tp}</div>
              <div className="text-xs text-slate-300">
                Pigmentation risk: {r.pigmentation_risk.toFixed(2)}
              </div>
              <div className="text-xs text-slate-300">
                Acne risk: {r.acne_risk.toFixed(2)}
              </div>
              <div className="text-xs text-slate-300">
                Wrinkle risk: {r.wrinkle_risk.toFixed(2)}
              </div>
              {visuals?.[tp] && (
                <img
                  src={`data:image/png;base64,${visuals[tp]}`}
                  alt={`${tp} simulation`}
                  className="mt-2 rounded border border-slate-700"
                />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Simulator;


