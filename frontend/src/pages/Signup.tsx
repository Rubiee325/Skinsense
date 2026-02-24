import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signup } from "../api";

const Signup: React.FC = () => {
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        name: "",
        age: 25,
        gender: "male",
        role: "patient"
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === "age" ? parseInt(value) : value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            await signup(formData);
            navigate("/login");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Signup failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-[85vh] px-4 py-8">
            <div className="w-full max-w-lg p-8 space-y-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl shadow-2xl">
                <div className="text-center space-y-2">
                    <h1 className="text-3xl font-bold tracking-tight text-white">Create an account</h1>
                    <p className="text-slate-400">Join SkinMorph to track your skin health</p>
                </div>

                {error && (
                    <div className="p-3 text-sm text-red-400 bg-red-900/20 border border-red-900/50 rounded-lg">
                        {error}
                    </div>
                )}

                <form className="grid grid-cols-1 md:grid-cols-2 gap-4" onSubmit={handleSubmit}>
                    <div className="space-y-1 md:col-span-2">
                        <label className="text-sm font-medium text-slate-300">Full Name</label>
                        <input
                            name="name"
                            type="text"
                            placeholder="John Doe"
                            className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 outline-none transition-all"
                            value={formData.name}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="space-y-1 md:col-span-2">
                        <label className="text-sm font-medium text-slate-300">Email Address</label>
                        <input
                            name="email"
                            type="email"
                            placeholder="john@example.com"
                            className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 outline-none transition-all"
                            value={formData.email}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="space-y-1 md:col-span-2">
                        <label className="text-sm font-medium text-slate-300">Password</label>
                        <input
                            name="password"
                            type="password"
                            placeholder="••••••••"
                            className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 outline-none transition-all"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            minLength={6}
                        />
                    </div>

                    <div className="space-y-1">
                        <label className="text-sm font-medium text-slate-300">Age</label>
                        <input
                            name="age"
                            type="number"
                            className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 outline-none transition-all"
                            value={formData.age}
                            onChange={handleChange}
                            required
                            min={0}
                        />
                    </div>

                    <div className="space-y-1">
                        <label className="text-sm font-medium text-slate-300">Gender</label>
                        <select
                            name="gender"
                            className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 outline-none transition-all appearance-none"
                            value={formData.gender}
                            onChange={handleChange}
                            required
                        >
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div className="space-y-1 md:col-span-2">
                        <label className="text-sm font-medium text-slate-300">I am joining as a:</label>
                        <div className="grid grid-cols-2 gap-3 mt-1">
                            <button
                                type="button"
                                className={`py-2 px-4 rounded-xl border transition-all ${formData.role === "patient"
                                        ? "bg-teal-500/20 border-teal-500 text-teal-400"
                                        : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                                    }`}
                                onClick={() => setFormData(prev => ({ ...prev, role: "patient" }))}
                            >
                                Patient
                            </button>
                            <button
                                type="button"
                                className={`py-2 px-4 rounded-xl border transition-all ${formData.role === "dermatologist"
                                        ? "bg-teal-500/20 border-teal-500 text-teal-400"
                                        : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                                    }`}
                                onClick={() => setFormData(prev => ({ ...prev, role: "dermatologist" }))}
                            >
                                Dermatologist
                            </button>
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3 px-4 bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold rounded-xl shadow-lg shadow-teal-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed md:col-span-2 mt-2"
                    >
                        {loading ? "Creating account..." : "Create Account"}
                    </button>
                </form>

                <div className="text-center text-sm text-slate-400">
                    Already have an account?{" "}
                    <Link to="/login" className="text-teal-400 hover:text-teal-300 font-medium underline underline-offset-4">
                        Sign in
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Signup;
