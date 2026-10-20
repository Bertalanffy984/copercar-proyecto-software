from sqlalchemy.orm import Session
from app.repositories.usuarios_repositori.usuario_repository import UsuarioRepository
from app.utils.security import verificar_contrasena

def autenticar_usuario(db:Session, correo:str, contrasenia:str):
    usuario_buscado=UsuarioRepository.obtener_por_correo(db=db, correo=correo)
    if not usuario_buscado:
        return None
    if not verificar_contrasena(contrasena_plana=contrasenia, contrasena_hash = usuario_buscado.contrasena):
        return None
    return usuario_buscado