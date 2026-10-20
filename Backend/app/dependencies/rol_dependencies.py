from fastapi import Depends,status
from app.models.models_db.Usuario import Usuario
from app.dependencies.jwt_dependecia import obtener_usuario_activo
from app.utils.errores_http import errores


def obtener_administrador(usuario_actual: Usuario = Depends(obtener_usuario_activo)) -> Usuario:
  if usuario_actual.id_rol != 1:
    raise errores["acceso_denegado"]
  return usuario_actual