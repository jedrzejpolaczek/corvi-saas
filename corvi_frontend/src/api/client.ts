import axios from "axios";
export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "/api" });
export function auth(token?: string){ if(token){ api.defaults.headers.common["Authorization"] = `Bearer ${token}`; } return api; }
