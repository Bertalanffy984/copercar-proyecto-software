from app.schemas.base import *


class DepartamentoBase(ConConfigBaseModel):
  nombre: str = Field(..., max_length=50)


class DepartamentoResponse(DepartamentoBase):
  id_departamento: int