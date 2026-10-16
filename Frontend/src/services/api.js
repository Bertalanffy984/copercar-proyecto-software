export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// Punto de integración preparado para el backend FastAPI descrito en la arquitectura.
// Mientras el backend no esté conectado, la aplicación utiliza datos de demostración
// persistidos en localStorage a través de AppDataContext.
export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  if (!response.ok) throw new Error(`Error HTTP ${response.status}`)
  return response.status === 204 ? null : response.json()
}
