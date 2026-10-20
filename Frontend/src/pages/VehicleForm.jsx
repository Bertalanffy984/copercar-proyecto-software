import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAppData } from '../context/AppDataContext'
import PageTitle from '../components/PageTitle'
import SearchableSelect from '../components/SearchableSelect'

const empty = { title:'',status:'Disponible',brand:'',line:'',color:'',year:new Date().getFullYear(),plate:'',mileage:'',price:'',owners:1,engine:'',fuel:'',transmission:'',department:'VALLE DEL CAUCA',city:'Cali',photos:[],soatNumber:'',soatExpiry:'',rtmNumber:'',rtmExpiry:'' }
import { brands, linesByBrand, citiesByDepartment, departments } from '../data/catalogs'

const fuels=['Gasolina','Diésel','Híbrida','Eléctrico']
const transmissions=['Automática','Mecánica']

export default function VehicleForm() {
  const { id } = useParams(); const navigate = useNavigate()
  const { vehicles, addVehicle, updateVehicle, loadingVehicles } = useAppData()
  const existing = useMemo(()=>vehicles.find(v=>v.id===Number(id)),[vehicles,id])
  const [form,setForm]=useState(existing ? {...existing} : empty)
  useEffect(() => { if (existing) setForm({...existing}) }, [existing?.id])
  const [error,setError]=useState('')
  const [saving,setSaving]=useState(false)
  const editing=!!existing
  const change=(key,val)=>setForm(f=>({...f,[key]:val}))
  const submit=async e=>{
    e.preventDefault(); setError('')
    if(!form.title||!form.plate||!form.brand||!form.line||!form.color||!form.price||!form.mileage) return setError('Complete todos los campos obligatorios.')
    if(!/^[A-Z]{3}[0-9]{3}$/i.test(form.plate.trim())) return setError('La placa debe tener 3 letras seguidas de 3 números (ejemplo: ABC123).')
    if(Number(form.price)<=0 || Number(form.mileage)<0 || Number(form.owners)<1 || !form.engine || !form.fuel || !form.transmission || !departments.includes(form.department) || !form.city.trim()) return setError('Revise los campos obligatorios y los valores numéricos.')
    if(Number(form.year)<1950 || Number(form.year)>new Date().getFullYear()+1) return setError('El año del modelo está fuera del rango permitido.')
    const duplicate=vehicles.some(v=>v.plate.toLowerCase()===form.plate.trim().toLowerCase() && v.id!==form.id)
    if(duplicate) return setError('Ya existe un vehículo registrado con esta placa.')
    const payload={...form,plate:form.plate.trim().toUpperCase(),price:Number(form.price),mileage:Number(form.mileage),owners:Number(form.owners)}
    setSaving(true)
    try {
      if (editing) await updateVehicle(payload)
      else await addVehicle(payload)
      navigate('/vehiculos')
    } catch (e) { setError(e.message || 'No se pudo guardar el vehículo.') }
    finally { setSaving(false) }
  }
  const onFiles=async e=>{
    const files=[...e.target.files].slice(0,8)
    const read=f=>new Promise(res=>{const r=new FileReader();r.onload=()=>res(r.result);r.readAsDataURL(f)})
    const data=await Promise.all(files.map(read)); change('photos',[...(form.photos||[]),...data])
  }
  if(id && !existing && loadingVehicles) return null
  if(id && !existing) return <section className="page-section"><h2>Vehículo no encontrado</h2><button className="btn btn-orange" onClick={()=>navigate('/vehiculos')}>Volver al inventario</button></section>
  return (
    <section className="page-section form-page">
      <PageTitle>{editing?'Editar vehículo':'Agregar vehículo'}</PageTitle>
      <form onSubmit={submit}>
        <div className="vehicle-form-grid">
          <label className="field"><span>Nombre o título*</span><input value={form.title} onChange={e=>change('title',e.target.value)}/></label>
          <label className="field"><span>Estado*</span><select value={form.status} onChange={e=>change('status',e.target.value)}><option>Disponible</option><option>Ingresando</option><option>No disponible</option><option>Vendido</option><option>Separado</option></select></label>
          <label className="field"><span>Marca*</span><select value={form.brand} onChange={e=>setForm(f=>({...f,brand:e.target.value,line:''}))}><option value="">Marca</option>{brands.map(x=><option key={x}>{x}</option>)}</select></label>
          <label className="field"><span>Línea*</span><input list="vehicle-lines" value={form.line} onChange={e=>change('line',e.target.value)}/><datalist id="vehicle-lines">{(linesByBrand[form.brand]||[]).map(x=><option key={x} value={x}/>)}</datalist></label>
          <label className="field"><span>Color*</span><input value={form.color} onChange={e=>change('color',e.target.value)}/></label>
          <label className="field"><span>Modelo (Año)*</span><input type="number" min="1950" max="2035" value={form.year} onChange={e=>change('year',e.target.value)}/></label>
          <label className="field"><span>Placa*</span><input value={form.plate} onChange={e=>change('plate',e.target.value)}/></label>
          <label className="field"><span>Kilometraje*</span><input type="number" min="0" value={form.mileage} onChange={e=>change('mileage',e.target.value)}/></label>
          <label className="field"><span>Precio*</span><input type="number" min="0" value={form.price} onChange={e=>change('price',e.target.value)} placeholder="$"/></label>
          <label className="field"><span>Cant. dueños*</span><input type="number" min="1" value={form.owners} onChange={e=>change('owners',e.target.value)}/></label>
          <label className="field"><span>Cilindraje*</span><input value={form.engine} onChange={e=>change('engine',e.target.value)}/></label>
          <label className="field"><span>Combustible*</span><select value={form.fuel} onChange={e=>change('fuel',e.target.value)}><option value="">Combustible</option>{fuels.map(x=><option key={x}>{x}</option>)}</select></label>
          <label className="field"><span>Transmisión*</span><select value={form.transmission} onChange={e=>change('transmission',e.target.value)}><option value="">Transmisión</option>{transmissions.map(x=><option key={x}>{x}</option>)}</select></label>
          <label className="field"><span>Departamento de Matrícula*</span><SearchableSelect value={form.department} options={departments} onChange={department=>setForm(f=>({...f,department,city:department===f.department?f.city:''}))} placeholder="Buscar departamento" ariaLabel="Departamento de matrícula" /></label>
          <label className="field"><span>Ciudad o municipio de Matrícula*</span><SearchableSelect value={form.city} options={citiesByDepartment[form.department]||[]} onChange={city=>change('city',city)} placeholder="Buscar o escribir municipio" ariaLabel="Ciudad o municipio de matrícula" allowCustom disabled={!form.department}/><small className="field-hint">Escribe para filtrar; si no aparece en las sugerencias, puedes ingresar el municipio manualmente.</small></label>
        </div>
        <div className="photo-section"><label className="btn btn-orange upload-label">+Agregar foto<input type="file" accept="image/*" multiple onChange={onFiles}/></label><div className="photo-grid">{(form.photos||[]).map((p,i)=><div className="photo-item" key={i}><img src={p}/><button type="button" onClick={()=>change('photos',form.photos.filter((_,j)=>j!==i))}>×</button></div>)}</div></div>
        <div className="doc-section"><h3>SOAT</h3><div className="doc-grid"><label className="field date-field" style={{gridColumn:'1 / -1'}}><span>Vigencia hasta</span><input type="date" value={form.soatExpiry} onChange={e=>change('soatExpiry',e.target.value)}/></label></div></div>
        <div className="doc-section"><h3>Revisión Tecnomecánica</h3><div className="doc-grid"><label className="field date-field" style={{gridColumn:'1 / -1'}}><span>Vigencia hasta</span><input type="date" value={form.rtmExpiry} onChange={e=>change('rtmExpiry',e.target.value)}/></label></div></div>
        {error&&<div className="form-error form-wide">{error}</div>}
        <div className="form-actions"><button className="btn btn-orange" disabled={saving}>Guardar</button><button className="btn btn-orange secondary-orange" type="button" onClick={()=>navigate('/vehiculos')}>Cancelar</button></div>
      </form>
    </section>
  )
}
