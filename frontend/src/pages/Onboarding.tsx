import React from "react";
import { Link } from "react-router-dom";

const Onboarding: React.FC = () => {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Welcome to SkinMorph</h1>
      <p className="text-sm text-slate-300">
        This is a research prototype for skin image analysis and risk
        simulation. It is not a medical device and does not replace a
        dermatologist.
      </p>
      <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">
        <li>Capture clear, well-lit photos of a single lesion or skin area.</li>
        <li>We will run detection, risk prediction, and recommendations.</li>
        <li>
          No photos are sent to remote servers unless you explicitly configure
          it.
        </li>
      </ul>
      <Link
        className="inline-flex px-4 py-2 rounded-md bg-teal-500 text-slate-950 text-sm font-medium hover:bg-teal-400"
        to="/capture"
      >
        Get started
      </Link>
    </div>
  );
};

export default Onboarding;






