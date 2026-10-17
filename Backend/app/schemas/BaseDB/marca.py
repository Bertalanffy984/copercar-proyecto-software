from app.schemas.base import *


class MarcaBase(ConConfigBaseModel):
  nombre: str = Field(..., max_length=50)


class MarcaResponse(MarcaBase):
  id_marca: int