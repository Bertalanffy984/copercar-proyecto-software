from fastapi import Depends,status
from app.models.models_db.Usuario import Usuario
from app.dependencies.jwt_dependecies import obtener_usuario_activo
from app.utils.respuestas_http_util import error_http


def obtener_administrador(usuario_actual: Usuario = Depends(obtener_usuario_activo)) -> Usuario:
  if usuario_actual.id_rol != 1:
    raise error_http("acceso_denegado")
  return usuario_actual