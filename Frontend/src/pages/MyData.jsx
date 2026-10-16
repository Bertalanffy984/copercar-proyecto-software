import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useAppData } from '../context/AppDataContext'

export default function MyData(){
 const {currentUser,updateSessionUser}=useAuth(); const {updateUser}=useAppData(); const [form,setForm]=useState({...currentUser}); const [saved,setSaved]=useState(false); const change=(k,v)=>{setSaved(false);setForm(f=>({...f,[k]:v}))}
 const submit=e=>{e.preventDefault();updateUser(form);updateSessionUser(form);setSaved(true)}
 return <section className="page-section"><div className="tabs-row"><button className="tab active">Mis datos</button></div><form onSubmit={submit} className="mydata-form"><div className="mydata-grid">
  <label className="field"><span>Tipo de documento*</span><select value={form.documentType} onChange={e=>change('documentType',e.target.value)}><option>Cédula</option><option>Pasaporte</option></select></label><label className="field"><span>Número de documento*</span><input value={form.documentNumber} onChange={e=>change('documentNumber',e.target.value)}/></label><label className="field"><span>Primer nombre*</span><input value={form.firstName} onChange={e=>change('firstName',e.target.value)}/></label>
  <label className="field"><span>Segundo nombre</span><input value={form.secondName||''} onChange={e=>change('secondName',e.target.value)}/></label><label className="field"><span>Primer Apellido*</span><input value={form.lastName} onChange={e=>change('lastName',e.target.value)}/></label><label className="field"><span>Segundo apellido</span><input value={form.secondLastName||''} onChange={e=>change('secondLastName',e.target.value)}/></label>
  <label className="field"><span>Fecha de nacimiento</span><input type="date" value={form.birthDate} onChange={e=>change('birthDate',e.target.value)}/></label><label className="field"><span>Número de celular*</span><input value={form.phone} onChange={e=>change('phone',e.target.value)}/></label><label className="field"><span>Género</span><select value={form.gender} onChange={e=>change('gender',e.target.value)}><option>Masculino</option><option>Femenino</option><option>Otro</option></select></label>
  <label className="field"><span>Dirección*</span><input value={form.address} onChange={e=>change('address',e.target.value)}/></label>
 </div>{saved&&<div className="success-note">Datos actualizados correctamente.</div>}<div className="form-actions"><button className="btn btn-orange">Guardar</button><button type="button" className="btn btn-orange secondary-orange" onClick={()=>setForm({...currentUser})}>Cancelar</button></div></form></section>
}
