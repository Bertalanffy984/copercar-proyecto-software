from app.utils.errores_http import errores
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.usuarios_repositori.usuario_repository import UsuarioRepository
from app.schemas.BaseDB.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.utils.security import obtener_hash_contrasena

class UsuarioService:
    id_rol_asesor=2
    
    @staticmethod
    def crear_usuario(db:Session, usuario_in:UsuarioCreate)->UsuarioResponse:
        if UsuarioRepository.obtener_por_documento(db=db, numero_documento=usuario_in.numero_documento):
            raise errores["usuario_doc_existe"]
        if UsuarioRepository.obtener_por_correo(db=db, correo=usuario_in.correo):
            raise errores["usuario_correo_existe"]
        contra_nueva_hasheada=obtener_hash_contrasena(usuario_in.contrasena)
        try:
            return UsuarioRepository.crear_usuario(
                db=db,
                usuario_in=usuario_in,
                id_rol_asesor=UsuarioService.id_rol_asesor,
                hash_pwd=contra_nueva_hasheada
            )
        except IntegrityError:
            db.rollback()
            raise errores["error_integridad_usuarios"]
    @staticmethod
    def buscar_por_documento(db:Session, numero_documento:int)->UsuarioResponse | None:
        usuario_buscado=UsuarioRepository.obtener_por_documento(db=db, numero_documento=numero_documento)
        if not usuario_buscado:
            raise errores["usuario_doc_no_existe"]
        return usuario_buscado
    
    @staticmethod
    def listar_usuarios(db:Session,skip:int=0, limit:int=20)->list[UsuarioResponse]:
        usuarios_listados=UsuarioRepository.listar_todos_asesores(db=db, skip=skip, limit=limit)
        return usuarios_listados
    
    @staticmethod
    def actualizar_usuario(db: Session, id_usuario:int, usuario_in: UsuarioUpdate) -> UsuarioResponse:
        usuario_buscado=UsuarioRepository.obtener_por_id(db=db, id_usuario=id_usuario)
        if not usuario_buscado:
            raise errores["usuario_id_no_existe"]
        
        if usuario_in.numero_documento and usuario_in.numero_documento!=usuario_buscado.numero_documento:
            if UsuarioRepository.obtener_por_documento(db=db,numero_documento=usuario_in.numero_documento):
                raise errores["usuario_doc_existe"]
        
        if usuario_in.correo and usuario_in.correo!=usuario_buscado.correo:
            if UsuarioRepository.obtener_por_correo(db=db, correo=usuario_in.correo):
                raise errores["usuario_correo_existe"]
        
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
            raise errores["usuario_id_no_existe"]
        UsuarioRepository.eliminar_asesor_completamente(db=db,db_usaurio=usuario_buscado)
        return{"exito": "El usuario se ha eliminado correctamente (204)"}