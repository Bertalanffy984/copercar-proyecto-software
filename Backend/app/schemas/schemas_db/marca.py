from app.schemas.base import *
from app.schemas.schemas_db.linea import LineaResponse

class MarcaUpdate(ConConfigBaseModel):
  nombre: str = Field(..., min_length=2, max_length=100)

  @field_validator("nombre")
  @classmethod
  def limpiar_texto(cls, v: str) -> str:
    return v.strip().upper()


class MarcaResponse(ConConfigBaseModel):
  id_marca: int
  nombre: str
  lineas: list[LineaResponse] = []