import React, { useState } from "react";
import { api } from "../api";

const Referral: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const resp = await api.get("/report", { responseType: "blob" });
      const blob = new Blob([resp.data], { type: "application/pdf" });
      const url = URL.createObjectURL(blob);
      setPdfUrl(url);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Clinician handoff</h2>
      <p className="text-sm text-slate-300">
        Generate a PDF snapshot of your current analysis and timeline that you
        can bring to a dermatologist. This does not replace a formal clinical
        note.
      </p>
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="inline-flex px-4 py-2 rounded-md bg-teal-500 text-slate-950 text-sm font-medium disabled:opacity-60"
      >
        {loading ? "Preparing PDF..." : "Generate PDF report"}
      </button>
      {pdfUrl && (
        <div className="space-y-2 text-sm">
          <a
            href={pdfUrl}
            target="_blank"
            rel="noreferrer"
            className="underline"
          >
            Open report in new tab
          </a>
          <p className="text-xs text-slate-400">
            You can print or save this PDF and share it with your clinician.
          </p>
        </div>
      )}
    </div>
  );
};

export default Referral;






