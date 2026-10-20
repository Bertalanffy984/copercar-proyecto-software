import { useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAppData } from '../context/AppDataContext'
import { useAuth } from '../context/AuthContext'
import PageTitle from '../components/PageTitle'
import SearchableSelect from '../components/SearchableSelect'

export default function MovementForm(){
 const {id}=useParams(); const navigate=useNavigate(); const {currentUser}=useAuth(); const {movements,vehicles,addMovement,updateMovement}=useAppData();
 const existing=useMemo(()=>movements.find(m=>m.id===Number(id)),[movements,id]);
 // Ningún vehículo se selecciona implícitamente al registrar una operación.
 const [form,setForm]=useState(existing?{...existing}:{vehicleId:'',type:'Compra',date:'',value:'',observation:''}); const [error,setError]=useState(''); const editing=!!existing;
 const selected=vehicles.find(v=>v.id===Number(form.vehicleId));
 const change=(k,v)=>setForm(f=>({...f,[k]:v}));
 const submit=e=>{e.preventDefault();setError('');if(!form.vehicleId||!form.type||!form.date||!form.value)return setError('Complete todos los campos obligatorios.');if(!Number.isFinite(Number(form.value))||Number(form.value)<=0)return setError('El valor de la operación debe ser mayor que cero.');const v=vehicles.find(x=>x.id===Number(form.vehicleId));if(!v)return setError('Seleccione un vehículo registrado en el inventario.');const payload={...form,vehicleId:Number(form.vehicleId),value:Number(form.value),vehicle:v?.title||existing?.vehicle,plate:v?.plate||existing?.plate,user:editing?existing.user:`${currentUser.firstName} ${currentUser.lastName}`,userId:editing?existing.userId:currentUser.id};try { editing?updateMovement({...existing,...payload}):addMovement(payload);navigate('/movimientos') } catch(e) { setError(e.message || 'No se pudo guardar el movimiento.') }}
 if(id && (!existing || existing.deleted)) return <section className="page-section"><h2>Movimiento no encontrado</h2><button className="btn btn-green" onClick={()=>navigate('/movimientos')}>Volver</button></section>
 return <section className="page-section form-page"><PageTitle>{editing?'Editar movimiento':'Movimientos'}</PageTitle>
  {!editing&&<div className="subtab active">Registrar movimiento</div>}
  <form className="movement-form card-outline" onSubmit={submit}><h1>{editing?'Editar movimiento':'Registrar movimiento'}</h1>
   {editing&&<div className="movement-current"><b>Vehículo:</b> {existing.vehicle}<br/><b>Placa:</b> {existing.plate}</div>}
   <div className="movement-two"><label className="field"><span>Seleccionar vehículo *</span><SearchableSelect value={form.vehicleId} options={vehicles.map(v=>({value:String(v.id),label:`${v.plate} · ${v.title} (${v.year})`}))} onChange={value=>change('vehicleId',Number(value))} placeholder="Buscar por placa o nombre" ariaLabel="Buscar vehículo por placa o nombre" />{editing && <small className="field-hint">Puedes corregir el vehículo asociado. Su placa y nombre se actualizarán en el movimiento.</small>}</label><label className="field"><span>Tipo de movimiento *</span><select value={form.type} onChange={e=>change('type',e.target.value)}><option>Compra</option><option>Venta</option></select></label></div>
   <label className="field movement-short"><span>Fecha del movimiento</span><input type="date" value={form.date} onChange={e=>change('date',e.target.value)}/></label>
   <label className="field movement-short"><span>Valor de la operación</span><input type="number" min="1" value={form.value} onChange={e=>change('value',e.target.value)} placeholder="$"/></label>
   <label className="field"><span>Observación</span><textarea rows="4" value={form.observation} onChange={e=>change('observation',e.target.value)} placeholder="Observación..."></textarea></label>
   {error&&<div className="form-error">{error}</div>}
   <div className="form-actions right"><button className="btn btn-green">Guardar</button><button type="button" className="btn btn-light" onClick={()=>navigate('/movimientos')}>Cancelar</button></div>
  </form>
 </section>
}
