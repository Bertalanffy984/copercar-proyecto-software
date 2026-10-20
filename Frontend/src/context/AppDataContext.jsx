import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { demoMovements, demoUsers, demoVehicles } from '../data/mockData'
import { demoKey } from '../data/demoStorage'
import { useAuth } from './AuthContext'
import { backendMode } from '../services/api'
import { listarVehiculosBackend, crearVehiculoBackend, actualizarVehiculoBackend, eliminarVehiculoBackend } from '../services/backend'
import { fromBackendVehicle, toBackendVehicle } from '../services/backendCatalogs'

const AppDataContext = createContext(null)
const load = (key, fallback) => {
  try { return JSON.parse(localStorage.getItem(key)) || fallback } catch { return fallback }
}

export function AppDataProvider({ children }) {
  const {currentUser} = useAuth()
  const [vehicles, setVehicles] = useState(() => backendMode ? [] : load(demoKey('vehicles'), demoVehicles))
  const [loadingVehicles, setLoadingVehicles] = useState(false)
  const [vehicleError, setVehicleError] = useState('')
  const [movements, setMovements] = useState(() => backendMode ? [] : load(demoKey('movements'), demoMovements))
  const [users, setUsers] = useState(() => backendMode ? [] : load(demoKey('users'), demoUsers))
  useEffect(() => { if (backendMode) setUsers(currentUser ? [currentUser] : []) }, [currentUser])

  useEffect(() => { if (!backendMode) localStorage.setItem(demoKey('vehicles'), JSON.stringify(vehicles)) }, [vehicles])

  // Solo los endpoints disponibles de FastAPI se conectan a MySQL.
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
    let cancelled = false
    setLoadingVehicles(true); setVehicleError('')
    listarVehiculosBackend().then(result => { if (!cancelled) setVehicles(result.filter(x => x.activo).map(fromBackendVehicle)) })
      .catch(e => { if (!cancelled) setVehicleError(e.message) })
      .finally(() => { if (!cancelled) setLoadingVehicles(false) })
    return () => { cancelled = true }
  }, [currentUser?.id])
  useEffect(() => { if (!backendMode) localStorage.setItem(demoKey('movements'), JSON.stringify(movements)) }, [movements])
  useEffect(() => { if (!backendMode) localStorage.setItem(demoKey('users'), JSON.stringify(users)) }, [users])

  const addVehicle = async v => {
    if (backendMode) { const saved = await crearVehiculoBackend(toBackendVehicle(v)); await refreshVehicles(); return fromBackendVehicle(saved) }
    setVehicles(prev => [...prev, { ...v, id: Math.max(0, ...prev.map(x => x.id)) + 1 }])
    return v
  }
  const updateVehicle = async v => {
    if (backendMode) {
      const previous = vehicles.find(x => x.id === v.id)
      if (!previous) throw new Error('Vehículo no encontrado en la lista actual.')
      const saved = await actualizarVehiculoBackend(v.id, toBackendVehicle(v, previous))
      await refreshVehicles(); return fromBackendVehicle(saved)
    }
    setVehicles(prev => prev.map(x => x.id === v.id ? v : x))
    return v
  }
  const deleteVehicle = async id => {
    if (backendMode) {
      await eliminarVehiculoBackend(id)
      await refreshVehicles()
      return true
    }
    if (movements.some(m => m.vehicleId === id)) return false
    setVehicles(prev => prev.filter(x => x.id !== id))
    return true
  }

  const syncSales = (all) => {
    if (backendMode) return
    setVehicles(prev => prev.map(v => {
      const activeSales = all.some(m => !m.deleted && m.vehicleId === v.id && m.type === 'Venta')
      if (activeSales) return { ...v, status: 'Vendido', demoPreviousStatus: v.demoPreviousStatus || (v.status === 'Vendido' ? 'Disponible' : v.status) }
      if (v.demoPreviousStatus) {
        const { demoPreviousStatus, ...rest } = v
        return { ...rest, status: demoPreviousStatus }
      }
      return v
    }))
  }
  const addMovement = m => {
    if (backendMode) throw new Error('FastAPI todavía no ofrece crear movimientos. No se guardó el movimiento.')
    const next = [...movements, { ...m, deleted: false, id: Math.max(0, ...movements.map(x => x.id)) + 1 }]
    setMovements(next); syncSales(next)
  }
  const updateMovement = m => {
    if (backendMode) throw new Error('FastAPI todavía no ofrece editar movimientos. No se guardó el cambio.')
    const next = movements.map(x => x.id === m.id ? m : x)
    setMovements(next); syncSales(next)
  }
  const deleteMovement = id => {
    if (backendMode) throw new Error('FastAPI todavía no ofrece eliminar movimientos.')
    const next = movements.map(x => x.id === id ? { ...x, deleted: true } : x)
    setMovements(next); syncSales(next)
  }

  const addUser = u => { if (backendMode) throw new Error('FastAPI todavía no ofrece crear usuarios. No se guardó el usuario.'); setUsers(prev => [...prev, { ...u, id: Math.max(0, ...prev.map(x => x.id)) + 1, role: u.role || 'asesor' }]) }
  const updateUser = u => { if (backendMode) throw new Error('FastAPI todavía no ofrece actualizar usuarios. No se guardaron cambios.'); setUsers(prev => prev.map(x => x.id === u.id ? { ...x, ...u, password: u.password || x.password } : x)) }
  const deleteUser = id => {
    if (backendMode) throw new Error('FastAPI todavía no ofrece eliminar usuarios.')
    if (users.find(u => u.id === id)?.role === 'admin' && users.filter(u => u.role === 'admin').length <= 1) return false
    setUsers(prev => prev.filter(x => x.id !== id))
    return true
  }

  const resetDemo = () => {
    if (backendMode) return
    setVehicles(demoVehicles); setMovements(demoMovements); setUsers(demoUsers)
  }

  const value = useMemo(() => ({ vehicles, loadingVehicles, vehicleError, refreshVehicles, movements, users, addVehicle, updateVehicle, deleteVehicle, addMovement, updateMovement, deleteMovement, addUser, updateUser, deleteUser, resetDemo }), [vehicles, movements, users, loadingVehicles, vehicleError])
  return <AppDataContext.Provider value={value}>{children}</AppDataContext.Provider>
}

export const useAppData = () => useContext(AppDataContext)
