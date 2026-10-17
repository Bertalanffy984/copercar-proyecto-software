from app.schemas.base import *
from app.schemas.BaseDB.marca import MarcaResponse


class LineaBase(ConConfigBaseModel):
  id_marca: int
  nombre: str = Field(..., max_length=50)


class LineaResponse(LineaBase):
  id_linea: int
  marca: Optional[MarcaResponse] = None