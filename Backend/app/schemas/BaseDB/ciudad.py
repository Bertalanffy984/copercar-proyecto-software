from app.schemas.base import *
from app.schemas.BaseDB.departamento import DepartamentoResponse


class CiudadBase(ConConfigBaseModel):
  id_departamento: int
  nombre: str = Field(..., max_length=50)


class CiudadResponse(CiudadBase):
  id_ciudad: int
  departamento: Optional[DepartamentoResponse] = None