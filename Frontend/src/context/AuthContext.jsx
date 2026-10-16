import { createContext, useContext, useMemo, useState } from 'react'
import { demoUsers } from '../data/mockData'
import { demoKey, sessionKey } from '../data/demoStorage'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(() => {
    try { const saved = JSON.parse(sessionStorage.getItem(sessionKey)); if (!saved) return null; const { password: ignoredPassword, ...safe } = saved; return safe } catch { return null }
  })

  const login = (email, password) => {
    const stored = JSON.parse(localStorage.getItem(demoKey('users')) || 'null') || demoUsers
    const user = stored.find(u => u.email.toLowerCase() === email.trim().toLowerCase() && u.password === password)
    if (!user) return { ok: false, message: 'Correo electrónico o contraseña incorrectos' }
    const { password: ignoredPassword, ...safeUser } = user
    setCurrentUser(safeUser)
    sessionStorage.setItem(sessionKey, JSON.stringify(safeUser))
    return { ok: true, user: safeUser }
  }

  const logout = () => {
    sessionStorage.removeItem(sessionKey)
    setCurrentUser(null)
  }

  const updateSessionUser = (user) => {
    const { password: ignoredPassword, ...safeUser } = user
    setCurrentUser(safeUser)
    sessionStorage.setItem(sessionKey, JSON.stringify(safeUser))
  }

  const value = useMemo(() => ({ currentUser, login, logout, updateSessionUser }), [currentUser])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
