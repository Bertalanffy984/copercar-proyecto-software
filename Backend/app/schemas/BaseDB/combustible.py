from app.schemas.base import *


class CombustibleBase(ConConfigBaseModel):
  nombre: str = Field(..., max_length=30)


class CombustibleResponse(CombustibleBase):
  id_combustible: int