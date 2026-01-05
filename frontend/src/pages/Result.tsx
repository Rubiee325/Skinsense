import React from "react";
import { useLocation, Link } from "react-router-dom";

interface LocationState {
  result?: any;
  rawImage?: string | null;
}

const Result: React.FC = () => {
  const location = useLocation();
  const state = location.state as LocationState | null;

  const prediction = state?.result?.prediction;
  const recs = state?.result?.recommendations ?? [];

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Analysis result</h2>
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <p className="text-sm text-slate-300">Original image</p>
          {state?.rawImage && (
            <img
              src={state.rawImage}
              alt="Original"
              className="rounded-lg border border-slate-800"
            />
          )}
        </div>
        <div className="space-y-2">
          <p className="text-sm text-slate-300">Grad-CAM focus map</p>
          {prediction?.gradcam_overlay_png_b64 && (
            <img
              src={`data:image/png;base64,${prediction.gradcam_overlay_png_b64}`}
              alt="Grad-CAM"
              className="rounded-lg border border-slate-800"
            />
          )}
        </div>
      </div>
      {prediction && (
        <div className="space-y-2">
          <h3 className="font-medium text-lg">Top finding</h3>
          <p className="text-sm">
            {prediction.top_class.label} —{" "}
            {(prediction.top_class.probability * 100).toFixed(1)}%
          </p>
        </div>
      )}
      <div className="space-y-2">
        <h3 className="font-medium text-lg">Personalized suggestions</h3>
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
      <div className="flex gap-3 text-sm">
        <Link className="underline" to="/simulator" state={state}>
          View future simulation
        </Link>
        <Link className="underline" to="/timeline">
          Go to timeline
        </Link>
        <Link className="underline" to="/referral" state={state}>
          Export for clinician
        </Link>
      </div>
    </div>
  );
};

export default Result;






