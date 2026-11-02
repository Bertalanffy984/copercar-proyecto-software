import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { demoMovements, demoUsers, demoVehicles } from '../data/mockData'
import { demoKey } from '../data/demoStorage'
import { useAuth } from './AuthContext'
import { backendMode } from '../services/api'
import {
  listarVehiculosBackend, crearVehiculoBackend, actualizarVehiculoBackend, eliminarVehiculoBackend,
  listarUsuariosBackend, crearUsuarioBackend, actualizarUsuarioBackend, desactivarUsuarioBackend,
  listarMovimientosBackend, crearMovimientoBackend, actualizarMovimientoBackend, eliminarMovimientoBackend,
  subirFotoVehiculoBackend,
} from '../services/backend'
import { fromBackendVehicle, toBackendVehicle } from '../services/backendCatalogs'

const AppDataContext = createContext(null)
const load = (key, fallback) => {
  try { return JSON.parse(localStorage.getItem(key)) || fallback } catch { return fallback }
}

// Las fotos del formulario siguen teniendo el mismo aspecto, pero las nuevas
// son data: URLs que se suben DESPUÉS de crear el vehículo (requiere ID).
const pendingPhotos = form => (form.photos || []).filter(p => typeof p === 'string' && p.startsWith('data:image/'))
async function uploadNewPhotos(id, form, existingPhotos = []) {
  const pending = pendingPhotos(form)
  if (!pending.length) return
  let sent = 0
  for (const [index, value] of pending.entries()) {
    try {
      const file = await fetch(value).then(response => response.blob())
      await subirFotoVehiculoBackend(id, file, existingPhotos.length + index, !existingPhotos.length && index === 0)
      sent += 1
    } catch (error) {
      throw new Error('Los datos del vehículo se guardaron correctamente, pero no se pudieron cargar todas las fotografías. Intenta agregarlas nuevamente desde Editar vehículo.')
    }
  }
}

export function AppDataProvider({ children }) {
  const { currentUser } = useAuth()
  const [vehicles, setVehicles] = useState(() => backendMode ? [] : load(demoKey('vehicles'), demoVehicles))
  const [loadingVehicles, setLoadingVehicles] = useState(false)
  const [vehicleError, setVehicleError] = useState('')
  const [movements, setMovements] = useState(() => backendMode ? [] : load(demoKey('movements'), demoMovements))
  const [loadingMovements, setLoadingMovements] = useState(false)
  const [movementError, setMovementError] = useState('')
  const [users, setUsers] = useState(() => backendMode ? [] : load(demoKey('users'), demoUsers))
  const [loadingUsers, setLoadingUsers] = useState(false)
  const [usersError, setUsersError] = useState('')

  useEffect(() => { if (!backendMode) localStorage.setItem(demoKey('vehicles'), JSON.stringify(vehicles)) }, [vehicles])
  useEffect(() => { if (!backendMode) localStorage.setItem(demoKey('movements'), JSON.stringify(movements)) }, [movements])
  useEffect(() => { if (!backendMode) localStorage.setItem(demoKey('users'), JSON.stringify(users)) }, [users])

  const refreshVehicles = async () => {
    if (!backendMode) return
    setLoadingVehicles(true); setVehicleError('')
    try {
      const result = await listarVehiculosBackend()
      setVehicles(result.filter(x => x.activo).map(fromBackendVehicle))
    } catch (e) { setVehicleError(e.message); throw e }
    finally { setLoadingVehicles(false) }
  }
  useEffect(() => {
    if (!backendMode) return
    if (!currentUser) { setVehicles([]); setVehicleError(''); return }
    let active = true
    setLoadingVehicles(true); setVehicleError('')
    listarVehiculosBackend().then(result => { if (active) setVehicles(result.filter(x=>x.activo).map(fromBackendVehicle)) })
      .catch(e => { if (active) setVehicleError(e.message) })
      .finally(() => { if (active) setLoadingVehicles(false) })
    return () => { active = false }
  }, [currentUser?.id])

  const refreshUsers = async () => {
    if (!backendMode || currentUser?.role !== 'admin') return
    setLoadingUsers(true); setUsersError('')
    try {
      const result = await listarUsuariosBackend()
      // Gestión de usuarios del backend solo devuelve asesores; las bajas se ocultan del listado operativo.
      setUsers(result.filter(u => u.active))
    } catch (e) { setUsersError(e.message); throw e }
    finally { setLoadingUsers(false) }
  }
  useEffect(() => {
    if (!backendMode) return
    if (currentUser?.role !== 'admin') { setUsers([]); setUsersError(''); return }
    let active = true
    setLoadingUsers(true); setUsersError('')
    listarUsuariosBackend().then(result => { if (active) setUsers(result.filter(u => u.active)) })
      .catch(e => { if (active) setUsersError(e.message) })
      .finally(() => { if (active) setLoadingUsers(false) })
    return () => { active = false }
  }, [currentUser?.id, currentUser?.role])

  const refreshMovements = async (list = vehicles) => {
    if (!backendMode || currentUser?.role !== 'admin') return
    setLoadingMovements(true); setMovementError('')
    try { setMovements(await listarMovimientosBackend(list)) }
    catch (e) { setMovementError(e.message); throw e }
    finally { setLoadingMovements(false) }
  }
  useEffect(() => {
    if (!backendMode) return
    if (currentUser?.role !== 'admin') {
      setMovements([])
      setMovementError('')
      return
    }
    if (loadingVehicles) return
    let active = true
    setLoadingMovements(true); setMovementError('')
    listarMovimientosBackend(vehicles).then(result => { if (active) setMovements(result) })
      .catch(e => { if (active) setMovementError(e.message) })
      .finally(() => { if (active) setLoadingMovements(false) })
    return () => { active = false }
  }, [currentUser?.id, currentUser?.role, vehicles, loadingVehicles])

  const addVehicle = async v => {
    if (backendMode) {
      const saved = await crearVehiculoBackend(toBackendVehicle(v))
      try { await uploadNewPhotos(saved.id_vehiculo, v) }
      finally { await refreshVehicles() }
      return fromBackendVehicle(saved)
    }
    setVehicles(prev => [...prev, { ...v, id:Math.max(0,...prev.map(x=>x.id))+1 }])
    return v
  }
  const updateVehicle = async v => {
    if (backendMode) {
      const previous = vehicles.find(x => x.id === v.id)
      if (!previous) throw new Error('Vehículo no encontrado en el inventario actual.')
      const removed = (previous.photos || []).filter(p => !(v.photos || []).includes(p))
      if (removed.length) throw new Error('El backend no dispone de una ruta para eliminar fotografías anteriores. Consérvelas; sí puede agregar nuevas.')
      const saved = await actualizarVehiculoBackend(v.id, toBackendVehicle(v, previous))
      try { await uploadNewPhotos(v.id, v, previous.photos || []) }
      finally { await refreshVehicles() }
      return fromBackendVehicle(saved)
    }
    setVehicles(prev => prev.map(x => x.id === v.id ? v : x))
    return v
  }
  const deleteVehicle = async id => {
    if (backendMode) { await eliminarVehiculoBackend(id); await refreshVehicles(); return true }
    if (movements.some(m => m.vehicleId === id)) return false
    setVehicles(prev => prev.filter(x => x.id !== id)); return true
  }

  const syncSales = all => {
    if (backendMode) return
    setVehicles(prev => prev.map(v => {
      const sale = all.some(m => !m.deleted && m.vehicleId === v.id && m.type === 'Venta')
      if (sale) return {...v,status:'Vendido',demoPreviousStatus:v.demoPreviousStatus || (v.status==='Vendido'?'Disponible':v.status)}
      if (v.demoPreviousStatus) { const {demoPreviousStatus,...rest}=v;return {...rest,status:demoPreviousStatus} }
      return v
    }))
  }
  const addMovement = async m => {
    if (backendMode) { const saved=await crearMovimientoBackend(m); await refreshMovements(); return saved }
    const next=[...movements,{...m,deleted:false,id:Math.max(0,...movements.map(x=>x.id))+1}]
    setMovements(next);syncSales(next);return m
  }
  const updateMovement = async m => {
    if (backendMode) { const saved=await actualizarMovimientoBackend(m.id,m);await refreshMovements();return saved }
    const next=movements.map(x=>x.id===m.id?m:x);setMovements(next);syncSales(next);return m
  }
  const deleteMovement = async id => {
    if (backendMode) { await eliminarMovimientoBackend(id);await refreshMovements();return true }
    const next=movements.map(x=>x.id===id?{...x,deleted:true}:x);setMovements(next);syncSales(next);return true
  }
  const addUser = async u => {
    if (backendMode) { const saved=await crearUsuarioBackend(u);await refreshUsers();return saved }
    setUsers(prev=>[...prev,{...u,id:Math.max(0,...prev.map(x=>x.id))+1,role:u.role||'asesor'}]);return u
  }
  const updateUser = async u => {
    if (backendMode) { const saved=await actualizarUsuarioBackend(u.id,u);await refreshUsers();return saved }
    setUsers(prev=>prev.map(x=>x.id===u.id?{...x,...u,password:u.password||x.password}:x));return u
  }
  const deleteUser = async id => {
    if (backendMode) {
      const target=users.find(u=>u.id===id)
      if (!target || target.role==='admin') throw new Error('Solo se permite dar de baja a asesores registrados en el listado.')
      await desactivarUsuarioBackend(id);await refreshUsers();return true
    }
    if (users.find(u=>u.id===id)?.role==='admin' && users.filter(u=>u.role==='admin').length<=1) return false
    setUsers(prev=>prev.filter(x=>x.id!==id));return true
  }
  const resetDemo = () => { if (!backendMode) {setVehicles(demoVehicles);setMovements(demoMovements);setUsers(demoUsers)} }

  const value = useMemo(() => ({
    vehicles, loadingVehicles, vehicleError, refreshVehicles,
    movements, loadingMovements, movementError, refreshMovements,
    users, loadingUsers, usersError, refreshUsers,
    addVehicle, updateVehicle, deleteVehicle,
    addMovement, updateMovement, deleteMovement,
    addUser, updateUser, deleteUser, resetDemo,
  }), [vehicles,movements,users,loadingVehicles,vehicleError,loadingMovements,movementError,loadingUsers,usersError,currentUser?.id])
  return <AppDataContext.Provider value={value}>{children}</AppDataContext.Provider>
}
export const useAppData = () => useContext(AppDataContext)
