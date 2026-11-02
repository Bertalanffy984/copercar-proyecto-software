from app.utils.respuestas_http_util import error_http
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.usuarios_repositories.usuario_repositories import UsuarioRepository
from app.schemas.schemas_db.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.utils.security_util import obtener_hash_contrasena

class UsuarioService:
    @staticmethod
    def crear_usuario(db:Session, usuario_in:UsuarioCreate)->UsuarioResponse:
        if UsuarioRepository.obtener_por_documento(db=db, numero_documento=usuario_in.numero_documento):
            raise error_http("usuario_doc_existe")
        if UsuarioRepository.obtener_por_correo(db=db, correo=usuario_in.correo):
            raise error_http("usuario_correo_existe")
        contra_nueva_hasheada=obtener_hash_contrasena(usuario_in.contrasena)
        try:
            return UsuarioRepository.crear_usuario(
                db = db,
                usuario_in = usuario_in,
                hash_pwd = contra_nueva_hasheada
            )
        except IntegrityError:
            db.rollback()
            raise error_http("error_integridad_usuarios")
        
    @staticmethod
    def buscar_por_documento(db:Session, numero_documento:int)->UsuarioResponse | None:
        usuario_buscado=UsuarioRepository.obtener_por_documento(db=db, numero_documento=numero_documento)
        if not usuario_buscado:
            raise error_http("usuario_doc_no_existe")
        return usuario_buscado
    
    @staticmethod
    def listar_usuarios_filtrado(db:Session, id_rol:int | None, skip:int=0, limit:int=20)->list[UsuarioResponse]:
        usuarios_listados=UsuarioRepository.listar_todos_usuarios_filtrado(db=db,id_rol = id_rol, skip=skip, limit=limit)
        return usuarios_listados
    
    @staticmethod
    def actualizar_usuario(db: Session, id_usuario:int, usuario_in: UsuarioUpdate) -> UsuarioResponse:
        usuario_buscado=UsuarioRepository.obtener_por_id(db=db, id_usuario=id_usuario)
        if not usuario_buscado:
            raise error_http("usuario_id_no_existe")
        
        if usuario_in.numero_documento and usuario_in.numero_documento!=usuario_buscado.numero_documento:
            if UsuarioRepository.obtener_por_documento(db=db,numero_documento=usuario_in.numero_documento):
                raise error_http("usuario_doc_existe")
        
        if usuario_in.correo and usuario_in.correo!=usuario_buscado.correo:
            if UsuarioRepository.obtener_por_correo(db=db, correo=usuario_in.correo):
                raise error_http("usuario_correo_existe")
        
        contra_hash_actualizada=None
        
        if usuario_in.contrasena:
            contra_hash_actualizada=obtener_hash_contrasena(contrasena=usuario_in.contrasena)
        
        return UsuarioRepository.actualizar_usuario(
            db=db,
            db_usuario=usuario_buscado,
            usuario_in=usuario_in,
            contra_hash=contra_hash_actualizada
        )
        
    @staticmethod
    def eliminar_usuario(db:Session, id_usuario:int)->None:
        usuario_buscado=UsuarioRepository.obtener_por_id(db=db, id_usuario=id_usuario)
        if not usuario_buscado:
            raise error_http("usuario_id_no_existe")
        UsuarioRepository.desactivar_usuario(db=db,db_usuario=usuario_buscado)
        return{"exito": "El usuario se ha desactivado correctamente (204)"}