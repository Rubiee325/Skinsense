import React, { useEffect, useState } from "react";
import { api } from "../api";

interface EventItem {
  observation_id: number;
  captured_at: string;
  top_class?: string;
  top_prob?: number;
}

interface LesionItem {
  lesion_id: number;
  body_site?: string;
  notes?: string;
  events: EventItem[];
}

const Timeline: React.FC = () => {
  const [lesions, setLesions] = useState<LesionItem[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const { data } = await api.get("/timeline");
        setLesions(data.lesions ?? []);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Timeline</h2>
      <p className="text-sm text-slate-300">
        Longitudinal tracking of lesions and skin regions appears here as you
        upload images via the capture or upload flows.
      </p>
      {lesions.length === 0 && (
        <p className="text-xs text-slate-400">
          No events yet. Use the capture flow to start tracking.
        </p>
      )}
      <div className="space-y-4">
        {lesions.map((lesion) => (
          <div key={lesion.lesion_id}>
            <div className="text-sm font-medium">
              Lesion #{lesion.lesion_id}{" "}
              {lesion.body_site && (
                <span className="text-slate-400">({lesion.body_site})</span>
              )}
            </div>
            {lesion.notes && (
              <div className="text-xs text-slate-400 mb-1">{lesion.notes}</div>
            )}
            <div className="border-l border-slate-700 pl-4 space-y-2 mt-1">
              {lesion.events.map((ev) => (
                <div key={ev.observation_id} className="relative">
                  <span className="absolute -left-4 top-1 w-2 h-2 rounded-full bg-teal-400" />
                  <div className="text-xs text-slate-400">
                    {ev.captured_at}
                  </div>
                  <div className="text-xs">
                    {ev.top_class ?? "Unknown"}{" "}
                    {typeof ev.top_prob === "number" &&
                      `— ${(ev.top_prob * 100).toFixed(1)}%`}
                  </div>
                </div>
              ))}
              {lesion.events.length === 0 && (
                <div className="text-xs text-slate-500">
                  No observations yet.
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Timeline;


