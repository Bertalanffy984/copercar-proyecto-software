from app.schemas.base import *


class FotoVehiculoBase(ConConfigBaseModel):
  id_vehiculo: int
  ruta: str = Field(..., max_length=2048)
  public_id: str = Field(..., max_length=255)
  es_principal: bool = False
  orden: int = Field(0, ge=0)


class FotoVehiculoResponse(FotoVehiculoBase):
  id_foto: int