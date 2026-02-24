import axios from "axios";

const baseURL =
  (process.env.REACT_APP_API_BASE as string) || "http://localhost:8000";

export const api = axios.create({
  baseURL
});

// Add a request interceptor to include the JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("skinmorph_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export async function login(credentials: any) {
  const { data } = await api.post("/auth/login", credentials);
  if (data.access_token) {
    localStorage.setItem("skinmorph_token", data.access_token);
    localStorage.setItem("skinmorph_user", JSON.stringify(data.user));
    localStorage.setItem("skinmorph_role", data.user.role);
  }
  return data;
}

export async function signup(userData: any) {
  const { data } = await api.post("/auth/signup", userData);
  return data;
}

export function logout() {
  localStorage.removeItem("skinmorph_token");
  localStorage.removeItem("skinmorph_user");
  localStorage.removeItem("skinmorph_role");
  window.location.href = "/login";
}

export async function predict(file: File) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/predict", form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return data;
}

export async function getPatients() {
  const { data } = await api.get("/dermatologist/patients");
  return data;
}

export async function getPatientPredictions(patientId: string) {
  const { data } = await api.get(`/dermatologist/patient/${patientId}/predictions`);
  return data;
}

export async function predictSequence(files: File[]) {
  const form = new FormData();
  files.forEach((f) => form.append("files", f));
  const { data } = await api.post("/predict_sequence", form);
  return data;
}






