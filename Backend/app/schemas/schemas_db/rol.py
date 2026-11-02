from app.schemas.base import *


class RolBase(ConConfigBaseModel):
  nombre_rol: str = Field(..., max_length=30)
  descripcion: Optional[str] = Field(None, max_length=100)


class RolResponse(RolBase):
  id_rol: int