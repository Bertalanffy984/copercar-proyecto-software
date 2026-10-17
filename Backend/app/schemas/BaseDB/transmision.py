from app.schemas.base import *


class TransmisionBase(ConConfigBaseModel):
  nombre: str = Field(..., max_length=30)


class TransmisionResponse(TransmisionBase):
  id_transmision: int