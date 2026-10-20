// FastAPI solo ofrece las rutas de autenticacion e inventario indicadas en Swagger.
// El proxy de Vite reenvia /backend-api a http://127.0.0.1:8000 en desarrollo.
export const backendMode = import.meta.env.VITE_API_MODE === 'backend'
export const API_URL = backendMode ? (import.meta.env.VITE_API_URL || '/backend-api') : (import.meta.env.VITE_API_URL || 'http://localhost:8000/api')
export const apiTokenKey = 'copercar_backend_token'

export async function apiRequest(path, options = {}) {
  const { headers: suppliedHeaders, ...requestOptions } = options
  const headers = new Headers(suppliedHeaders || {})
  if (!headers.has('Content-Type') && requestOptions.body && !(requestOptions.body instanceof FormData)) {
    headers.set('Content-Type', requestOptions.body instanceof URLSearchParams ? 'application/x-www-form-urlencoded' : 'application/json')
  }
  const token = sessionStorage.getItem(apiTokenKey)
  if (token && !headers.has('Authorization')) headers.set('Authorization', `Bearer ${token}`)
  let response
  try { response = await fetch(`${API_URL}${path}`, { ...requestOptions, headers }) }
  catch { throw new Error('No se pudo conectar con FastAPI. Compruebe que el backend esta ejecutandose en el puerto 8000.') }
  const raw = await response.text()
  let result = null
  try { result = raw ? JSON.parse(raw) : null } catch { result = raw }
  if (!response.ok) {
    const detail = result?.detail
    const readable = Array.isArray(detail) ? detail.map(x => `${(x.loc||[]).join('.')}: ${x.msg}`).join('; ') : (typeof detail === 'string' ? detail : '')
    throw new Error(readable || `Error HTTP ${response.status}`)
  }
  return result
}
