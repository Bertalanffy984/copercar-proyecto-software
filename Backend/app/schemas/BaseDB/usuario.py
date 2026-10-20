from app.schemas.base import *
from app.schemas.BaseDB.rol import RolResponse


class UsuarioBase(ConConfigBaseModel):
  #id_rol: int
  tipo_documento: str = Field(..., max_length=4)
  numero_documento: str = Field(..., max_length=20)
  primer_nombre: str = Field(..., max_length=50)
  segundo_nombre: Optional[str] = Field(None, max_length=50)
  primer_apellido: str = Field(..., max_length=50)
  segundo_apellido: Optional[str] = Field(None, max_length=50)
  correo: str
  celular: str = Field(..., max_length=20)
  fecha_nacimiento: date
  genero: str = Field(..., max_length=20)
  direccion: str = Field(..., max_length=150)


class UsuarioCreate(UsuarioBase):
  contrasena: str = Field(..., min_length=6)


class UsuarioUpdate(ConConfigBaseModel):
  #id_rol: Optional[int] = None
  tipo_documento: Optional[str] = Field(None, max_length=4)
  numero_documento: Optional[str] = Field(None, max_length=20)
  primer_nombre: Optional[str] = Field(None, max_length=50)
  segundo_nombre: Optional[str] = Field(None, max_length=50)
  primer_apellido: Optional[str] = Field(None, max_length=50)
  segundo_apellido: Optional[str] = Field(None, max_length=50)
  correo: Optional[str] = None
  celular: Optional[str] = Field(None, max_length=20)
  fecha_nacimiento: Optional[date] = None
  genero: Optional[str] = Field(None, max_length=20)
  direccion: Optional[str] = Field(None, max_length=150)
  contrasena: Optional[str] = Field(None, min_length=6)
  activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
  id_usuario: int
  activo: bool
  fecha_registro: datetime
  rol: Optional[RolResponse] = None