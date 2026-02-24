import React, { useEffect, useState } from "react";
import { getPatients, getPatientPredictions } from "../api";

const DermatologistDashboard: React.FC = () => {
    const [patients, setPatients] = useState<any[]>([]);
    const [selectedPatient, setSelectedPatient] = useState<any | null>(null);
    const [predictions, setPredictions] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [detailsLoading, setDetailsLoading] = useState(false);

    useEffect(() => {
        const fetchPatients = async () => {
            try {
                const data = await getPatients();
                setPatients(data);
            } catch (err) {
                console.error("Failed to fetch patients", err);
            } finally {
                setLoading(false);
            }
        };
        fetchPatients();
    }, []);

    const handleViewPatient = async (patient: any) => {
        setSelectedPatient(patient);
        setDetailsLoading(true);
        try {
            const data = await getPatientPredictions(patient.id);
            setPredictions(data.predictions);
        } catch (err) {
            console.error("Failed to fetch predictions", err);
        } finally {
            setDetailsLoading(false);
        }
    };

    if (loading) {
        return <div className="flex items-center justify-center min-h-[50vh]">Loading patients...</div>;
    }

    return (
        <div className="space-y-6 max-w-5xl mx-auto px-4">
            <div className="flex justify-between items-end border-b border-slate-800 pb-4">
                <div>
                    <h1 className="text-2xl font-bold text-white">Dermatologist Dashboard</h1>
                    <p className="text-slate-400">Review patient history and analysis results</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Patient List */}
                <div className="lg:col-span-1 space-y-4">
                    <h2 className="text-lg font-semibold text-slate-300">Patients</h2>
                    <div className="space-y-2 max-h-[60vh] overflow-y-auto pr-2 custom-scrollbar">
                        {patients.length === 0 ? (
                            <p className="text-slate-500 text-sm">No patients found.</p>
                        ) : (
                            patients.map((patient) => (
                                <div
                                    key={patient.id}
                                    onClick={() => handleViewPatient(patient)}
                                    className={`p-4 rounded-xl border cursor-pointer transition-all ${selectedPatient?.id === patient.id
                                            ? "bg-teal-500/10 border-teal-500 shadow-lg shadow-teal-500/5"
                                            : "bg-slate-900/50 border-slate-800 hover:border-slate-700"
                                        }`}
                                >
                                    <p className="font-medium text-white">{patient.name}</p>
                                    <p className="text-xs text-slate-400">{patient.email}</p>
                                    <div className="flex gap-2 mt-2 text-[10px] uppercase tracking-wider font-semibold">
                                        <span className="px-2 py-0.5 bg-slate-800 rounded text-slate-300">{patient.age}y</span>
                                        <span className="px-2 py-0.5 bg-slate-800 rounded text-slate-300">{patient.gender}</span>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>

                {/* Patient Details / Reports */}
                <div className="lg:col-span-2 space-y-4">
                    {selectedPatient ? (
                        <>
                            <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl">
                                <h3 className="text-lg font-bold text-teal-400">Reports for {selectedPatient.name}</h3>
                                <p className="text-sm text-slate-400">Total analysis records: {predictions.length}</p>
                            </div>

                            {detailsLoading ? (
                                <div className="py-20 text-center text-slate-500">Loading analysis history...</div>
                            ) : predictions.length === 0 ? (
                                <div className="py-20 text-center text-slate-500 bg-slate-900/30 rounded-xl border border-dashed border-slate-800">
                                    No analysis records found for this patient.
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {predictions.map((pred) => (
                                        <div key={pred.id} className="p-5 bg-slate-900/50 border border-slate-800 rounded-2xl space-y-3">
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <p className="text-xs text-slate-500 mb-1">{new Date(pred.created_at).toLocaleString()}</p>
                                                    <h4 className="text-lg font-semibold text-white">{pred.predicted_disease}</h4>
                                                </div>
                                                <div className={`px-3 py-1 rounded-full text-xs font-bold ${pred.severity === "high" ? "bg-red-500/20 text-red-500" :
                                                        pred.severity === "medium" ? "bg-orange-500/20 text-orange-500" :
                                                            "bg-green-500/20 text-green-500"
                                                    }`}>
                                                    {pred.severity.toUpperCase()} RISK
                                                </div>
                                            </div>

                                            <div className="flex items-center gap-4">
                                                <div className="flex-1">
                                                    <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                                                        <div
                                                            className="bg-teal-500 h-full"
                                                            style={{ width: `${pred.confidence * 100}%` }}
                                                        />
                                                    </div>
                                                </div>
                                                <span className="text-sm font-mono text-teal-400">{(pred.confidence * 100).toFixed(1)}%</span>
                                            </div>

                                            <div className="pt-2 flex gap-4 overflow-x-auto pb-2">
                                                {pred.top_3_predictions?.map((item: any, idx: number) => (
                                                    <div key={idx} className="flex-none px-3 py-2 bg-slate-950 rounded-lg border border-slate-800">
                                                        <p className="text-[10px] text-slate-500 uppercase">{item.disease}</p>
                                                        <p className="text-xs font-semibold">{(item.probability * 100).toFixed(1)}%</p>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </>
                    ) : (
                        <div className="flex flex-col items-center justify-center min-h-[40vh] bg-slate-900/20 rounded-2xl border border-dashed border-slate-800 p-8 text-center">
                            <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-4">
                                <svg className="w-8 h-8 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                            </div>
                            <h3 className="text-lg font-medium text-slate-300">No Patient Selected</h3>
                            <p className="text-sm text-slate-500 max-w-xs mt-1">Select a patient from the list on the left to review their detailed skin analysis history.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default DermatologistDashboard;
