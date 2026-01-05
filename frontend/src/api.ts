import axios from "axios";

const baseURL =
  (process.env.REACT_APP_API_BASE as string) || "http://localhost:8000";

export const api = axios.create({
  baseURL
});

export async function predict(file: File) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/predict", form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return data;
}

export async function predictSequence(files: File[]) {
  const form = new FormData();
  files.forEach((f) => form.append("files", f));
  const { data } = await api.post("/predict_sequence", form);
  return data;
}






