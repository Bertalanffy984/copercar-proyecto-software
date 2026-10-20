import { useEffect, useMemo, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAppData } from '../context/AppDataContext'
import Modal from '../components/Modal'
import Pagination from '../components/Pagination'
import { DeleteAction, EditAction } from '../components/ActionIcons'
import { UserEditor } from './UserForm'

export default function Users() {
  const { users, deleteUser } = useAppData()
  const navigate = useNavigate()
  const location = useLocation()
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(1)
  const [toDelete, setToDelete] = useState(null)
  const [toEdit, setToEdit] = useState(null)
  const [notice, setNotice] = useState(location.state?.notice || '')
  const [deleteError,setDeleteError] = useState('')
  useEffect(() => {
    if (location.state?.editUserId) {
      const found = users.find(u => u.id === location.state.editUserId)
      if (found) setToEdit(found)
      navigate('/usuarios', { replace:true, state:null })
    }
  }, [location.state, navigate, users])
  const perPage = 7
  const filtered = useMemo(() => users.filter(u => String(u.documentNumber).includes(query.trim())), [users, query])
  const totalPages = Math.max(1, Math.ceil(filtered.length / perPage))
  const rows = filtered.slice((page - 1) * perPage, page * perPage)
  return <section className="page-section users-page">
    <div className="tabs-row"><button className="tab active" aria-current="page">Gestión de usuarios / listado</button>{!toEdit && <button className="tab" onClick={()=>navigate('/usuarios/nuevo')}>Agregar usuario</button>}</div>
    <div className="module-heading-row"><h1 className="orange-title">Usuarios</h1></div>
    {notice && <div className="success-note" role="status">{notice} <button className="notice-close" type="button" onClick={()=>setNotice('')} aria-label="Cerrar mensaje">×</button></div>}
    <div className="toolbar"><label className="searchbox"><span>⌕</span><input value={query} onChange={e=>{setQuery(e.target.value);setPage(1)}} placeholder="Buscar por número de documento" /></label>{!toEdit && <button className="btn btn-green push-right" onClick={()=>navigate('/usuarios/nuevo')}>＋ Agregar Usuario</button>}</div>
    <div className="responsive-table-wrap"><table className="data-table users-table"><thead><tr><th>No. Orden</th><th>Tipo de Documento</th><th>Número de Documento</th><th>Nombre Completo</th><th>Correo Electrónico</th><th>Celular</th><th>Acciones</th></tr></thead><tbody>{rows.map((u,i)=><tr key={u.id}><td>{String((page-1)*perPage+i+1).padStart(2,'0')}</td><td>{u.documentType}</td><td>{u.documentNumber}</td><td>{u.firstName} {u.lastName}</td><td>{u.email}</td><td>{u.phone}</td><td className="table-actions"><EditAction onClick={()=>{setNotice('');setToEdit(u)}}/><DeleteAction onClick={()=>{setDeleteError('');setToDelete(u)}}/></td></tr>)}</tbody></table>{!rows.length && <div className="empty-state">No se encontraron usuarios.</div>}</div><Pagination page={page} totalPages={totalPages} onChange={setPage}/>
    <Modal open={!!toEdit} title={`Editar usuario${toEdit ? ` · ${toEdit.firstName} ${toEdit.lastName}` : ''}`} wide onClose={()=>setToEdit(null)}>
      {toEdit && <UserEditor key={toEdit.id} user={toEdit} onSaved={()=>{setToEdit(null);setNotice('Usuario modificado correctamente.')}} onCancel={()=>setToEdit(null)}/>}
    </Modal>
    <Modal open={!!toDelete} onClose={()=>setToDelete(null)}><div className="warning-symbol">⚠</div><p className="modal-question centered">¿Está seguro de que desea eliminar este usuario?</p>{toDelete && <div className="detail-list"><span>Nombre completo:</span><b>{toDelete.firstName} {toDelete.lastName}</b><span>Tipo de documento:</span><b>{toDelete.documentType}</b><span>Número de documento:</span><b>{toDelete.documentNumber}</b><span>Correo electrónico:</span><b>{toDelete.email}</b></div>}{toDelete?.role === 'admin' && users.filter(u=>u.role === 'admin').length <= 1 && <p className="form-error">No se puede eliminar al último administrador.</p>}{deleteError && <div className="form-error">{deleteError}</div>}<div className="modal-actions centered"><button className="btn btn-danger" disabled={!!toDelete && toDelete.role === 'admin' && users.filter(u=>u.role === 'admin').length <= 1} onClick={()=>{try{if(deleteUser(toDelete.id))setNotice('Usuario eliminado correctamente.');setToDelete(null)}catch(e){setDeleteError(e.message)}}}>Sí</button><button className="btn btn-gray" onClick={()=>setToDelete(null)}>No</button></div></Modal>
  </section>
}
