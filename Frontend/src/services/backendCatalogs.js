// Identificadores verificados contra COPERCAR.sql, version de prueba copercar_pruebas_v7.
// No hay endpoints GET de catalogos en la version actual de FastAPI.
// Si cambian las tablas de catalogos, pedir endpoints a backend y actualizar este mapa.
const normalize = value => String(value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim().toLowerCase().replace(/\s+/g,' ')

export const estadoBackendIds = { disponible:1, ingresando:2, separado:3, vendido:4, 'no disponible':5 }
const estados = estadoBackendIds
const combustibles = { diesel:2, electrico:3, gasolina:4, hibrida:1, hibrido:1 }
const transmisiones = { automatica:2, mecanica:1, manual:1 }
const ciudades = [
  { id:1, name:'Cali', dept:'VALLE DEL CAUCA' },
  { id:2, name:'Palmira', dept:'VALLE DEL CAUCA' },
  { id:3, name:'Tulua', dept:'VALLE DEL CAUCA' },
  { id:4, name:'Florencia', dept:'CAQUETÁ' },
]
const lineas = [
  {id:1,brand:'Mazda',name:'Mazda CX-30 Grand Touring LX'},
  {id:2,brand:'Mazda',name:'Mazda 2 Touring'},
  {id:3,brand:'Mazda',name:'Mazda 3 Sport'},
  {id:4,brand:'Toyota',name:'Corolla'},
  {id:5,brand:'Toyota',name:'Hilux'},
  {id:6,brand:'Renault',name:'Duster'},
  {id:7,brand:'Chevrolet',name:'Onix'},
  {id:8,brand:'Kia',name:'Picanto'},
  {id:9,brand:'Hyundai',name:'Tucson'},
  {id:10,brand:'BMW',name:'X1'},
]
const byNormalized = (record, value) => normalize(record) === normalize(value)
const required = (value, label) => { if (!value) throw new Error(label); return value }

export function fromBackendVehicle(v) {
  const brand = v.linea?.marca?.nombre || ''
  const department = normalize(v.ciudad?.departamento?.nombre) === 'caqueta' ? 'CAQUETÁ' : (v.ciudad?.departamento?.nombre?.toUpperCase() || '')
  return {
    id: v.id_vehiculo, title: v.titulo || '', status:v.estado?.nombre || '',
    brand, line:v.linea?.nombre || '', color:v.color || '',
    year:v.modelo, plate:v.placa, mileage:v.kilometraje,
    price:Number(v.precio), owners:v.cantidad_duenos, engine:v.cilindraje == null ? '' : String(v.cilindraje),
    fuel:({ Diesel:'Diésel', Electrico:'Eléctrico', Hibrido:'Híbrida', Gasolina:'Gasolina' })[v.combustible?.nombre] || v.combustible?.nombre || '',
    transmission:v.transmision?.nombre === 'Manual' ? 'Mecánica' : (v.transmision?.nombre === 'Automatica' ? 'Automática' : v.transmision?.nombre || ''),
    department, city:v.ciudad?.nombre || '',
    photos:[...(v.fotos||[])].sort((a,b)=>Number(b.es_principal)-Number(a.es_principal) || a.orden-b.orden).map(f=>f.ruta),
    soatNumber:'', soatExpiry:v.fecha_vencimiento_soat || '',
    rtmNumber:'', rtmExpiry:v.fecha_vencimiento_rtm || '',
  }
}

export function toBackendVehicle(form, original = null) {
  if (form.soatNumber?.trim() || form.rtmNumber?.trim()) {
    throw new Error('Los números de SOAT y RTM todavía no tienen campos ni endpoints en FastAPI. No se guardó el vehículo; deje esos números vacíos hasta que backend los implemente.')
  }
  const photos = form.photos || []
  const existingPhotos = original?.photos || []
  if (JSON.stringify(photos) !== JSON.stringify(existingPhotos)) {
    throw new Error('FastAPI todavía no ofrece subida, eliminación ni edición de fotografías. No se guardó el vehículo; conserve las fotos existentes y no adjunte nuevas por ahora.')
  }
  const brand = normalize(form.brand)
  const normalizedLine = normalize(form.line)
  const line = lineas.find(x => normalize(x.brand) === brand && (normalize(x.name) === normalizedLine || normalize(x.name).replace(`${brand} `, '') === normalizedLine))
  required(line, 'La línea y la marca seleccionadas no existen en el catálogo de la base MySQL de pruebas. Use una combinación ya registrada.')
  const city = ciudades.find(x=>byNormalized(x.name,form.city) && byNormalized(x.dept,form.department))
  required(city,'La ciudad y departamento seleccionados no existen en el catálogo MySQL de pruebas (Cali, Palmira, Tuluá o Florencia).')
  const idEstado = required(estados[normalize(form.status)], 'Estado de vehículo no reconocido.')
  const idCombustible = required(combustibles[normalize(form.fuel)], 'Combustible no reconocido.')
  const idTransmision = required(transmisiones[normalize(form.transmission)], 'Transmisión no reconocida.')
  const engine = String(form.engine||'').replace(',','.').trim()
  const engineValue = Number(engine)
  if (!Number.isFinite(engineValue) || engineValue < 0 || !engine || (engineValue <= 10 && engineValue !== 0 && !Number.isInteger(engineValue*1000))) {
    throw new Error('Cilindraje inválido: ingrese por ejemplo 1.8 o 1800.')
  }
  const cilindraje = engineValue <= 10 ? Math.round(engineValue*1000) : engineValue
  if (!Number.isInteger(cilindraje)) throw new Error('Cilindraje debe expresarse en centímetros cúbicos enteros.')
  return {
    id_linea:line.id, id_estado:idEstado, id_ciudad:city.id,
    titulo:form.title.trim(), placa:form.plate.trim().toUpperCase(),
    color:form.color.trim(), modelo:Number(form.year), kilometraje:Number(form.mileage),
    precio:Number(form.price), cantidad_duenos:Number(form.owners), cilindraje,
    id_combustible:idCombustible,id_transmision:idTransmision,
    fecha_vencimiento_soat:form.soatExpiry || null,
    fecha_vencimiento_rtm:form.rtmExpiry || null,
  }
}
