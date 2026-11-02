from app.schemas.base import *


class EstadoVehiculoBase(ConConfigBaseModel):
  nombre: str = Field(..., max_length=30)
  descripcion: Optional[str] = Field(None, max_length=100)


class EstadoVehiculoResponse(EstadoVehiculoBase):
  id_estado: int