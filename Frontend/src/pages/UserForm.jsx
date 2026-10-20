import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppData } from '../context/AppDataContext'
import PasswordField from '../components/PasswordField'

const empty = { documentType:'Cédula', documentNumber:'', firstName:'', secondName:'', lastName:'', secondLastName:'', email:'', phone:'', birthDate:'', gender:'Masculino', password:'', address:'', role:'asesor' }

// Reutilizable en la página "Agregar usuario" y en la ventana modal "Editar usuario".
export function UserEditor({ user = null, onSaved, onCancel }) {
  const { users, addUser, updateUser } = useAppData()
  const editing = Boolean(user)
  // Nunca precargar una contraseña al editar: FastAPI tampoco debe devolverla.
  const [form, setForm] = useState(() => user ? { ...user, password:'' } : { ...empty })
  const [error, setError] = useState('')
  const change = (key, value) => setForm(prev => ({ ...prev, [key]:value }))
  const submit = event => {
    event.preventDefault()
    setError('')
    const mandatory = ['documentType','documentNumber','firstName','lastName','email','phone','birthDate','gender','address']
    if (mandatory.some(key => !String(form[key] ?? '').trim()) || (!editing && !form.password.trim())) return setError('Complete todos los campos obligatorios.')
    if (new Date(`${form.birthDate}T12:00:00`) > new Date()) return setError('La fecha de nacimiento no puede ser futura.')
    if (!/^\S+@\S+\.\S+$/.test(form.email.trim())) return setError('Ingrese un correo válido.')
    if (users.some(u => u.email.toLowerCase() === form.email.trim().toLowerCase() && u.id !== user?.id)) return setError('Ya existe un usuario con este correo electrónico.')
    if (users.some(u => u.documentNumber.trim() === form.documentNumber.trim() && u.id !== user?.id)) return setError('Ya existe un usuario con ese número de documento.')
    const payload = { ...form, documentNumber:form.documentNumber.trim(), email:form.email.trim().toLowerCase() }
    try {
    if (editing) {
      // Sólo se envía password cuando se solicita cambiarla; la edición mantiene el rol.
      if (!payload.password) delete payload.password
      updateUser({ ...payload, role:user.role })
    } else addUser(payload)
    onSaved?.()
    } catch (e) { setError(e.message || 'No se pudo guardar el usuario.') }
  }
  return <form className="user-form" onSubmit={submit}>
    <h1>{editing ? 'Editar usuario' : 'Agregar usuario'}</h1>
    <div className="user-form-grid">
      <label className="field"><span>Tipo de documento *</span><select value={form.documentType} onChange={e=>change('documentType', e.target.value)}><option>Cédula</option><option>Pasaporte</option><option>Cédula de extranjería</option><option>NIT</option></select></label>
      <label className="field"><span>Correo electrónico *</span><input type="email" value={form.email} onChange={e=>change('email', e.target.value)} required /></label>
      <label className="field"><span>Número de documento *</span><input value={form.documentNumber} onChange={e=>change('documentNumber', e.target.value)} required /></label>
      <label className="field"><span>Número de celular *</span><input value={form.phone} onChange={e=>change('phone', e.target.value)} required /></label>
      <label className="field"><span>Primer nombre *</span><input value={form.firstName} onChange={e=>change('firstName', e.target.value)} required /></label>
      <label className="field"><span>Fecha de nacimiento *</span><input type="date" value={form.birthDate} onChange={e=>change('birthDate', e.target.value)} required /></label>
      <label className="field"><span>Segundo nombre (opcional)</span><input value={form.secondName || ''} onChange={e=>change('secondName', e.target.value)} /></label>
      <label className="field"><span>Género *</span><select value={form.gender} onChange={e=>change('gender', e.target.value)}><option>Masculino</option><option>Femenino</option></select></label>
      <label className="field"><span>Primer apellido *</span><input value={form.lastName} onChange={e=>change('lastName', e.target.value)} required /></label>
      <label className="field"><span>{editing ? 'Nueva contraseña (opcional)' : 'Contraseña *'}</span><PasswordField value={form.password} onChange={e=>change('password',e.target.value)} placeholder={editing ? 'Dejar vacía para conservar' : 'Digite la contraseña'} required={!editing}/>{editing && <small className="field-hint">Déjala vacía si no deseas cambiarla.</small>}</label>
      <label className="field"><span>Segundo apellido (opcional)</span><input value={form.secondLastName || ''} onChange={e=>change('secondLastName', e.target.value)} /></label>
      <label className="field"><span>Dirección *</span><input value={form.address} onChange={e=>change('address', e.target.value)} required /></label>
    </div>
    {error && <div className="form-error form-wide" role="alert">{error}</div>}
    <div className="form-actions right"><button type="submit" className="btn btn-green">Guardar</button><button type="button" className="btn btn-light" onClick={onCancel}>Cancelar</button></div>
  </form>
}

export default function UserForm() {
  const navigate = useNavigate()
  return <section className="page-section users-page"><div className="tabs-row"><button className="tab" onClick={()=>navigate('/usuarios')}>Gestión de usuarios / listado</button><button className="tab active" aria-current="page">Agregar usuario</button></div><UserEditor onSaved={()=>navigate('/usuarios', { state:{ notice:'Usuario agregado correctamente.' } })} onCancel={()=>navigate('/usuarios')} /></section>
}
