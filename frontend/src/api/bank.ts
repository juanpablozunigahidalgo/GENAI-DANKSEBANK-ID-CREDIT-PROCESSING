import axios from "axios";

// Ajusta el puerto si tu backend corre en otro
const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// 🧠 Chat con el agente
export const chatWithAgent = async (message: string, userId = "string") => {
  const res = await API.post("/chat/", {
    query: message,
    user_id: userId,
  });
  return res.data;
};

// 🪪 Subir ID — el user_id va en la QUERY, no en el FormData
export const uploadId = async (file: File, userId = "string") => {
  const formData = new FormData();
  formData.append("file", file);

  // 👇 importante: aquí va como query param
  const res = await API.post(`/upload-id/?user_id=${userId}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
};

// 👥 Obtener todos los clientes registrados
export const getAllCustomers = async () => {
  const res = await API.get("/customer/all");
  return res.data;
};

// 🔍 Consultar el registro nacional simulado
export const checkRegistry = async (nationalId: string, country: string) => {
  const res = await API.get("/registry/", {
    params: { national_id: nationalId, country },
  });
  return res.data;
};
