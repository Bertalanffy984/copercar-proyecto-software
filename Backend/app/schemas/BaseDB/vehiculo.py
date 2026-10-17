from app.schemas.base import *
from app.schemas.BaseDB.ciudad import CiudadResponse
from app.schemas.BaseDB.combustible import CombustibleResponse
from app.schemas.BaseDB.estado_vehiculo import EstadoVehiculoResponse
from app.schemas.BaseDB.foto_vehiculo import FotoVehiculoResponse
from app.schemas.BaseDB.linea import LineaResponse
from app.schemas.BaseDB.transmision import TransmisionResponse


class VehiculoBase(ConConfigBaseModel):
  id_linea: int
  id_estado: int
  id_ciudad: int
  titulo: str = Field(..., max_length=160)
  placa: str = Field(..., max_length=20)
  color: str = Field(..., max_length=30)
  modelo: int = Field(..., ge=1900, le=2100)
  kilometraje: int = Field(0, ge=0)
  precio: Decimal = Field(..., gt=0)
  cantidad_duenos: int = Field(0, ge=0)
  cilindraje: Optional[int] = Field(None, ge=0)
  id_combustible: int
  id_transmision: int
  fecha_vencimiento_soat: Optional[date] = None
  fecha_vencimiento_rtm: Optional[date] = None


class VehiculoCreate(VehiculoBase):
  pass


class VehiculoUpdate(ConConfigBaseModel):
  id_linea: Optional[int] = None
  id_estado: Optional[int] = None
  id_ciudad: Optional[int] = None
  titulo: Optional[str] = Field(None, max_length=160)
  placa: Optional[str] = Field(None, max_length=20)
  color: Optional[str] = Field(None, max_length=30)
  modelo: Optional[int] = Field(None, ge=1900, le=2100)
  kilometraje: Optional[int] = Field(None, ge=0)
  precio: Optional[Decimal] = Field(None, gt=0)
  cantidad_duenos: Optional[int] = Field(None, ge=0)
  cilindraje: Optional[int] = Field(None, ge=0)
  id_combustible: Optional[int] = None
  id_transmision: Optional[int] = None
  fecha_vencimiento_soat: Optional[date] = None
  fecha_vencimiento_rtm: Optional[date] = None
  activo: Optional[bool] = None


class VehiculoResponse(VehiculoBase):
  id_vehiculo: int
  activo: bool
  fecha_registro: datetime
  linea: Optional[LineaResponse] = None
  estado: Optional[EstadoVehiculoResponse] = None
  ciudad: Optional[CiudadResponse] = None
  combustible: Optional[CombustibleResponse] = None
  transmision: Optional[TransmisionResponse] = None
  fotos: List[FotoVehiculoResponse] = []