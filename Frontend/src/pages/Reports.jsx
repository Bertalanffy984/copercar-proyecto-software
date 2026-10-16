import { useMemo, useState } from 'react'
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'
import * as XLSX from 'xlsx'
import Modal from '../components/Modal'
import PageTitle from '../components/PageTitle'
import { useAppData } from '../context/AppDataContext'
import { formatCOP, formatDate } from '../utils/format'

function BarChart({ data }){
  const max=Math.max(...data.flatMap(d=>[d.income,d.expense]),1)
  return <div className="chart-card"><div className="chart-title">Ingresos y egresos</div><div className="chart-bars">{data.map(d=><div className="bar-group" key={d.month}><div className="bars"><i className="bar income" style={{height:`${Math.max(8,d.income/max*100)}%`}}/><i className="bar expense" style={{height:`${Math.max(6,d.expense/max*100)}%`}}/></div><small>{d.month.slice(0,3)}</small></div>)}</div><div className="chart-legend"><span><i className="legend income"/>Ingresos</span><span><i className="legend expense"/>Egresos</span></div></div>
}

export default function Reports(){
 const { movements, vehicles } = useAppData()
 const months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
 const [year,setYear]=useState('2026'); const [month,setMonth]=useState('Todos'); const [open,setOpen]=useState(false); const [format,setFormat]=useState('PDF')
 const yearMovements=useMemo(()=>movements.filter(m=>!m.deleted && m.date?.startsWith(`${year}-`)),[movements,year])
 const selectedMovements=useMemo(()=>yearMovements.filter(m=>month==='Todos'||Number(m.date.slice(5,7))===months.indexOf(month)+1),[yearMovements,month])
 const metrics=useMemo(()=>{const income=selectedMovements.filter(m=>m.type==='Venta').reduce((a,m)=>a+Number(m.value),0);const expense=selectedMovements.filter(m=>m.type==='Compra').reduce((a,m)=>a+Number(m.value),0);return {income,expense,gain:income-expense,count:selectedMovements.length}},[selectedMovements])
 const asRow = m => ({plate:m.plate || vehicles.find(v=>v.id===m.vehicleId)?.plate || '—',vehicle:m.vehicle || vehicles.find(v=>v.id===m.vehicleId)?.title || 'Vehículo',date:m.date,value:Number(m.value)})
 const soldVehicles=selectedMovements.filter(m=>m.type==='Venta').map(asRow)
 const boughtVehicles=selectedMovements.filter(m=>m.type==='Compra').map(asRow)
 const monthlyReport=months.map((name,i)=>{const records=yearMovements.filter(m=>Number(m.date.slice(5,7))===i+1);return {month:name,income:records.filter(m=>m.type==='Venta').reduce((a,m)=>a+Number(m.value),0),expense:records.filter(m=>m.type==='Compra').reduce((a,m)=>a+Number(m.value),0)}})
 const exportFile=()=>{
  if(format==='Excel'){
    const wb=XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb,XLSX.utils.json_to_sheet([{Periodo:`${month} ${year}`,Ingresos:metrics.income,Egresos:metrics.expense,Ganancia:metrics.gain,Movimientos:metrics.count}]),'Resumen')
    XLSX.utils.book_append_sheet(wb,XLSX.utils.json_to_sheet(soldVehicles),'Vendidos'); XLSX.utils.book_append_sheet(wb,XLSX.utils.json_to_sheet(boughtVehicles),'Comprados'); XLSX.writeFile(wb,`COPERCAR_reporte_${year}_${month}.xlsx`)
  }else{
    const doc=new jsPDF(); doc.setFontSize(18); doc.text('COPERCAR - Reporte',14,18); doc.setFontSize(11); doc.text(`Periodo: ${month} de ${year}`,14,28); doc.text(`Ingresos: ${formatCOP(metrics.income)}`,14,38); doc.text(`Egresos: ${formatCOP(metrics.expense)}`,14,45); doc.text(`Ganancia: ${formatCOP(metrics.gain)}`,14,52); doc.text(`Cantidad de movimientos: ${metrics.count}`,14,59);
    autoTable(doc,{startY:68,head:[['Tipo','Placa','Vehículo','Fecha','Valor']],body:[...soldVehicles.map(v=>['Venta',v.plate,v.vehicle,formatDate(v.date),formatCOP(v.value)]),...boughtVehicles.map(v=>['Compra',v.plate,v.vehicle,formatDate(v.date),formatCOP(v.value)])],styles:{fontSize:8},headStyles:{fillColor:[255,110,6]}})
    doc.save(`COPERCAR_reporte_${year}_${month}.pdf`)
  }
  setOpen(false)
 }
 return <section className="page-section"><PageTitle upper>REPORTES</PageTitle><div className="module-heading-row"><h1>Reportes</h1></div>
  <div className="report-filter-row"><label className="field compact"><span>Año</span><select value={year} onChange={e=>setYear(e.target.value)}>{Array.from(new Set([2026,...movements.map(m=>Number(m.date?.slice(0,4))).filter(Boolean)])).sort((a,b)=>b-a).map(y=><option key={y}>{y}</option>)}</select></label><label className="field compact"><span>Mes</span><select value={month} onChange={e=>setMonth(e.target.value)}>{['Todos',...months].map(m=><option key={m}>{m}</option>)}</select></label><button className="btn btn-green push-right" onClick={()=>setOpen(true)}>Exportar reporte</button></div>
  <div className="metric-grid"><div className="metric-card"><span>Ingresos (COP)</span><b className="green">{formatCOP(metrics.income)}</b></div><div className="metric-card"><span>Egresos (COP)</span><b className="red">{formatCOP(metrics.expense)}</b></div><div className="metric-card"><span>Ganancia (COP)</span><b className="blue">{formatCOP(metrics.gain)}</b></div><div className="metric-card"><span>Cantidad de movimientos</span><b>{metrics.count}</b></div></div>
  <BarChart data={monthlyReport}/><p className="report-explainer">Datos de demostración calculados a partir de movimientos activos. Ganancia = ingresos − egresos (saldo simple, no utilidad contable).</p>
  <h3 className="report-table-title">Vehículos vendidos</h3><div className="responsive-table-wrap"><table className="data-table compact-table"><thead><tr><th>Placa</th><th>Vehículo</th><th>Fecha</th><th>Valor</th></tr></thead><tbody>{soldVehicles.map((v,i)=><tr key={`${v.plate}-${i}`}><td>{v.plate}</td><td>{v.vehicle}</td><td>{formatDate(v.date)}</td><td>{formatCOP(v.value)}</td></tr>)}{!soldVehicles.length&&<tr><td colSpan="4">Sin ventas en el período seleccionado.</td></tr>}</tbody></table></div>
  <h3 className="report-table-title">Vehículos comprados</h3><div className="responsive-table-wrap"><table className="data-table compact-table"><thead><tr><th>Placa</th><th>Vehículo</th><th>Fecha</th><th>Valor</th></tr></thead><tbody>{boughtVehicles.map((v,i)=><tr key={`${v.plate}-${i}`}><td>{v.plate}</td><td>{v.vehicle}</td><td>{formatDate(v.date)}</td><td>{formatCOP(v.value)}</td></tr>)}{!boughtVehicles.length&&<tr><td colSpan="4">Sin compras en el período seleccionado.</td></tr>}</tbody></table></div>
  <Modal open={open} title="Exportar reporte" onClose={()=>setOpen(false)}><p>Periodo: {month} de {year}</p><p>Seleccione el formato</p><label className="radio-line"><input type="radio" checked={format==='PDF'} onChange={()=>setFormat('PDF')}/> PDF</label><label className="radio-line"><input type="radio" checked={format==='Excel'} onChange={()=>setFormat('Excel')}/> Excel</label><div className="modal-actions"><button className="btn btn-green" onClick={exportFile}>Exportar</button><button className="btn btn-gray" onClick={()=>setOpen(false)}>Cancelar</button></div></Modal>
 </section>
}
