import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { predict } from "../api";

const Capture: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
  };

  const handleSubmit = async () => {
    const file = fileInputRef.current?.files?.[0];
    if (!file) return;
    setLoading(true);
    try {
      const data = await predict(file);
      navigate("/result", { state: { result: data, rawImage: preview } });
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Capture or upload a photo</h2>
      <p className="text-sm text-slate-300">
        Align the lesion inside the guide box. Good lighting and focus improve
        results.
      </p>
      <div className="aspect-square w-full max-w-xs mx-auto border-2 border-dashed border-slate-700 rounded-xl flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-6 border border-teal-400/70 rounded-xl pointer-events-none" />
        {preview ? (
          <img
            src={preview}
            alt="Preview"
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-xs text-slate-400">
            Camera/Upload preview will appear here
          </span>
        )}
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="text-sm"
        onChange={handleFileChange}
      />
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="inline-flex px-4 py-2 rounded-md bg-teal-500 text-slate-950 text-sm font-medium disabled:opacity-60"
      >
        {loading ? "Analyzing..." : "Analyze image"}
      </button>
    </div>
  );
};

export default Capture;






