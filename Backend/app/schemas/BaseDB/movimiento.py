from app.schemas.base import *
from app.schemas.BaseDB.usuario import UsuarioResponse


class TipoMovimientoResponse(ConConfigBaseModel):
  id_tipo_movimiento: int
  nombre: str
  naturaleza: str
  descripcion: Optional[str] = None


class MovimientoBase(ConConfigBaseModel):
  id_vehiculo: int
  id_tipo_movimiento: int
  fecha_movimiento: date
  valor: Decimal = Field(...,decimal_places=2)
  observacion: Optional[str] = Field(None, max_length=1000)


class MovimientoCreate(MovimientoBase):
  pass


class MovimientoUpdate(ConConfigBaseModel):
  id_tipo_movimiento: Optional[int] = None
  fecha_movimiento: Optional[date] = None
  valor: Optional[Decimal] = Field(None, gt=0)
  observacion: Optional[str] = Field(None, max_length=1000)
  activo: Optional[bool] = None


class MovimientoResponse(MovimientoBase):
  id_movimiento: int
  id_usuario: int
  activo: bool
  tipo_movimiento: Optional[TipoMovimientoResponse] = None
  usuario: Optional[UsuarioResponse] = None