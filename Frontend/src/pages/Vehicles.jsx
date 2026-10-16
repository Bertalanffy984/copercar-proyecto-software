import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppData } from '../context/AppDataContext'
import Modal from '../components/Modal'
import PageTitle from '../components/PageTitle'
import StatusBadge from '../components/StatusBadge'
import { DeleteAction, EditAction } from '../components/ActionIcons'
import { formatCOP } from '../utils/format'

export default function Vehicles() {
  const { vehicles, movements, deleteVehicle } = useAppData()
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('Todos')
  const [toDelete, setToDelete] = useState(null)
  const filtered = useMemo(() => vehicles.filter(v => {
    const q = query.trim().toLowerCase()
    return (!q || v.plate.toLowerCase().includes(q) || v.title.toLowerCase().includes(q)) && (status==='Todos' || v.status===status)
  }), [vehicles, query, status])

  return (
    <section className="page-section">
      <PageTitle>Vehículos</PageTitle>
      <div className="toolbar vehicle-toolbar">
        <label className="searchbox"><span>⌕</span><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Buscar por placa" /></label>
        <label className="field compact"><span>Estado*</span><select value={status} onChange={e=>setStatus(e.target.value)}><option>Todos</option><option>Disponible</option><option>Ingresando</option><option>No disponible</option><option>Vendido</option><option>Separado</option></select></label>
        <button className="btn btn-green push-right" onClick={()=>navigate('/vehiculos/nuevo')}>Agregar Vehículo</button>
      </div>

      <div className="vehicle-list">
        {filtered.map((v, index) => (
          <article className="vehicle-row" key={v.id}>
            <div className="vehicle-index">{index+1}</div>
            <img className="vehicle-thumb" src={v.photos?.[0] || '/assets/ui/isotipo.png'} alt={v.title} />
            <div className="vehicle-info">
              <strong>{v.title}</strong>
              <span>Modelo {v.year}</span><span>{v.transmission}</span><span>{Number(v.mileage).toLocaleString('es-CO')} km</span>
              <span>Placa: {v.plate}</span><span>Precio {formatCOP(v.price)}</span>
            </div>
            <div className="vehicle-actions"><StatusBadge status={v.status}/><EditAction label="" onClick={()=>navigate(`/vehiculos/${v.id}/editar`)}/><DeleteAction label="" onClick={()=>setToDelete(v)}/></div>
          </article>
        ))}
        {!filtered.length && <div className="empty-state">No se encontraron vehículos para los criterios seleccionados.</div>}
      </div>

      <Modal open={!!toDelete} title="Eliminar vehículo" onClose={()=>setToDelete(null)}>
        <p className="modal-question">¿Está seguro de que desea eliminar este vehículo?</p>{toDelete && movements.some(m=>m.vehicleId===toDelete.id) && <p className="form-error">No se puede eliminar: tiene movimientos históricos asociados. Esta restricción protege la trazabilidad.</p>}
        {toDelete && <div className="modal-summary"><b>{toDelete.title}</b><span>Placa: {toDelete.plate}</span></div>}
        <div className="modal-actions"><button className="btn btn-danger" disabled={!!toDelete && movements.some(m=>m.vehicleId===toDelete.id)} onClick={()=>{deleteVehicle(toDelete.id);setToDelete(null)}}>Sí, eliminar</button><button className="btn btn-gray" onClick={()=>setToDelete(null)}>Cancelar</button></div>
      </Modal>
    </section>
  )
}
