import { apiRequest, apiTokenKey } from './api'

export async function loginBackend(email, password) {
  // OAuth2PasswordRequestForm: no enviar JSON a /auth/token.
  const body = new URLSearchParams({ username: email.trim(), password, grant_type: 'password' })
  const result = await apiRequest('/auth/token', { method: 'POST', body })
  if (!result?.access_token) throw new Error('El backend no devolvio un token de acceso.')
  sessionStorage.setItem(apiTokenKey, result.access_token)
  try { return await getBackendUser() }
  catch (error) { sessionStorage.removeItem(apiTokenKey); throw error }
}

export async function getBackendUser() {
  const data = await apiRequest('/auth/me')
  return {
    id: data.id_usuario, role: Number(data.id_rol) === 1 ? 'admin' : 'asesor',
    documentType: {CC:'Cédula',CE:'Cédula de extranjería',PAS:'Pasaporte',NIT:'NIT'}[data.tipo_documento] || data.tipo_documento,
    documentNumber: data.numero_documento || '',
    firstName: data.primer_nombre || '', secondName: data.segundo_nombre || '',
    lastName: data.primer_apellido || '', secondLastName: data.segundo_apellido || '',
    email: data.correo, phone: data.celular || '',
    birthDate: data.fecha_nacimiento || '', gender: data.genero || '',
    address: data.direccion || '', active: data.activo,
  }
}

export async function listarVehiculosBackend() {
  // FastAPI limita cada pagina a 20 vehiculos. Recuperar las paginas completas.
  const all = []
  const limit = 20
  for (let skip = 0; skip < 10000; skip += limit) {
    const page = await apiRequest(`/vehiculos/listar_activos?skip=${skip}&limit=${limit}`)
    if (!Array.isArray(page)) throw new Error('Respuesta inesperada del inventario.')
    all.push(...page)
    if (page.length < limit) return all
  }
  throw new Error('Inventario demasiado grande para la paginacion configurada.')
}

export const crearVehiculoBackend = data => apiRequest('/vehiculos/crear', { method:'POST', body:JSON.stringify(data) })
export const actualizarVehiculoBackend = (id, data) => apiRequest(`/vehiculos/actualizar/${encodeURIComponent(id)}`, {method:'PUT', body:JSON.stringify(data)})
export const eliminarVehiculoBackend = id => apiRequest(`/vehiculos/eliminar/${encodeURIComponent(id)}`, {method:'DELETE'})
export const buscarVehiculoBackend = placa => apiRequest(`/vehiculos/placa/${encodeURIComponent(placa)}`)
export const filtrarVehiculoBackend = estadoId => apiRequest(`/vehiculos/filtrar/estado/${encodeURIComponent(estadoId)}`)
