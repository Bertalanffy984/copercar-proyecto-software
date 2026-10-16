import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import PasswordField from '../components/PasswordField'

export default function Login() {
  const { currentUser, login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  if (currentUser) return <Navigate to="/vehiculos" replace />

  const submit = e => {
    e.preventDefault(); setError('')
    const result = login(email, password)
    if (!result.ok) return setError(result.message)
    navigate('/vehiculos', { replace: true })
  }

  return (
    <div className="login-page">
      <div className="login-brandbar"><img src="/assets/ui/logo-wordmark.png" alt="COPERCAR" /></div>
      <div className="login-center">
        <form className="login-card" onSubmit={submit}>
          <div className="login-hero"><img src="/assets/ui/isotipo.png" alt="COPERCAR" /></div>
          <input value={email} onChange={e=>setEmail(e.target.value)} type="email" placeholder="Digite el correo electrónico" aria-label="Correo electrónico" required />
          <PasswordField value={password} onChange={e=>setPassword(e.target.value)} placeholder="Digite la contraseña" required autoComplete="current-password" />
          {error && <div className="form-error">{error}</div>}
          <button className="btn btn-orange login-button">Iniciar</button>
          <div className="demo-help">Demo administrador: admin@copercar.com / Admin123*<br/>Demo asesor: asesor@copercar.com / Asesor123*</div>
        </form>
      </div>
    </div>
  )
}
