from app.schemas.base import *

class LineaCreate(ConConfigBaseModel):
  nombre: str = Field(..., min_length=2, max_length=100)
  id_marca: int

  @field_validator("nombre")
  @classmethod
  def limpiar_texto(cls, v: str) -> str:
    return v.strip().upper()

class LineaUpdate(ConConfigBaseModel):
  nombre: str | None = Field(None, min_length=2, max_length=100)
  id_marca: int | None = None

  @field_validator("nombre")
  @classmethod
  def limpiar_texto(cls, v: str | None) -> str | None:
    return v.strip().upper() if v else None

class LineaResponse(ConConfigBaseModel):
  id_linea: int
  nombre: str
  id_marca: int