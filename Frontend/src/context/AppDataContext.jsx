import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { demoMovements, demoUsers, demoVehicles } from '../data/mockData'
import { demoKey } from '../data/demoStorage'

const AppDataContext = createContext(null)
const load = (key, fallback) => {
  try { return JSON.parse(localStorage.getItem(key)) || fallback } catch { return fallback }
}

export function AppDataProvider({ children }) {
  const [vehicles, setVehicles] = useState(() => load(demoKey('vehicles'), demoVehicles))
  const [movements, setMovements] = useState(() => load(demoKey('movements'), demoMovements))
  const [users, setUsers] = useState(() => load(demoKey('users'), demoUsers))

  useEffect(() => localStorage.setItem(demoKey('vehicles'), JSON.stringify(vehicles)), [vehicles])
  useEffect(() => localStorage.setItem(demoKey('movements'), JSON.stringify(movements)), [movements])
  useEffect(() => localStorage.setItem(demoKey('users'), JSON.stringify(users)), [users])

  const addVehicle = v => setVehicles(prev => [...prev, { ...v, id: Math.max(0, ...prev.map(x => x.id)) + 1 }])
  const updateVehicle = v => setVehicles(prev => prev.map(x => x.id === v.id ? v : x))
  const deleteVehicle = id => {
    if (movements.some(m => m.vehicleId === id)) return false
    setVehicles(prev => prev.filter(x => x.id !== id))
    return true
  }

  const syncSales = (all) => {
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
    const next = [...movements, { ...m, deleted: false, id: Math.max(0, ...movements.map(x => x.id)) + 1 }]
    setMovements(next); syncSales(next)
  }
  const updateMovement = m => {
    const next = movements.map(x => x.id === m.id ? m : x)
    setMovements(next); syncSales(next)
  }
  const deleteMovement = id => {
    const next = movements.map(x => x.id === id ? { ...x, deleted: true } : x)
    setMovements(next); syncSales(next)
  }

  const addUser = u => setUsers(prev => [...prev, { ...u, id: Math.max(0, ...prev.map(x => x.id)) + 1, role: u.role || 'asesor' }])
  const updateUser = u => setUsers(prev => prev.map(x => x.id === u.id ? { ...x, ...u, password: u.password || x.password } : x))
  const deleteUser = id => {
    if (users.find(u => u.id === id)?.role === 'admin' && users.filter(u => u.role === 'admin').length <= 1) return false
    setUsers(prev => prev.filter(x => x.id !== id))
    return true
  }

  const resetDemo = () => {
    setVehicles(demoVehicles); setMovements(demoMovements); setUsers(demoUsers)
  }

  const value = useMemo(() => ({ vehicles, movements, users, addVehicle, updateVehicle, deleteVehicle, addMovement, updateMovement, deleteMovement, addUser, updateUser, deleteUser, resetDemo }), [vehicles, movements, users])
  return <AppDataContext.Provider value={value}>{children}</AppDataContext.Provider>
}

export const useAppData = () => useContext(AppDataContext)
