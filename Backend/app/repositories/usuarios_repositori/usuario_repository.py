from sqlalchemy.orm import Session
from app.models.models_db.Usuario import Usuario
from sqlalchemy.orm import Session
from app.models.models_db.Usuario import Usuario
from app.schemas.BaseDB.usuario import UsuarioCreate, UsuarioUpdate

class UsuarioRepository:
    
    @staticmethod
    def obtener_por_documento(db: Session, numero_documento: str) -> Usuario|None:
        return (
        db.query(Usuario).filter(Usuario.numero_documento == numero_documento).first()
    )
    @staticmethod
    def obtener_por_correo(db:Session,correo:str)-> Usuario | None:
        return db.query(Usuario).filter(Usuario.correo == correo).first() 
    
    @staticmethod
    def obtener_por_id(db: Session, id_usuario: int) -> Usuario | None:
        return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    
    @staticmethod
    def listar_todos_asesores(db:Session, skip:int=0, limit:int = 20)->list[Usuario]:
        return(
            db.query(Usuario)
            .filter(Usuario.id_rol==2)
            .offset(skip)
            .limit(limit).all()
        )
        
    @staticmethod
    def crear_usuario(db: Session, usuario_in: UsuarioCreate, id_rol_asesor: int, hash_pwd: str) -> Usuario:
        datos_dict=usuario_in.model_dump()
        datos_dict.pop("contrasena", None)
        asesor_user=Usuario(
            **datos_dict,
            contrasena=hash_pwd,
            id_rol=id_rol_asesor,
            activo=True
        )
        db.add(asesor_user)
        db.commit()
        db.refresh(asesor_user)
        return asesor_user
    
    @staticmethod
    def actualizar_usuario(db: Session, db_usuario: Usuario, usuario_in: UsuarioUpdate, contra_hash: str | None) -> Usuario:
       datos_actualizar = usuario_in.model_dump(exclude_unset=True)
       if "contrasena" in datos_actualizar:
         datos_actualizar.pop("contrasena")
         if contra_hash:
           db_usuario.contrasena = contra_hash

       for campo, valor in datos_actualizar.items():
         setattr(db_usuario, campo, valor)

       db.commit()
       db.refresh(db_usuario)
       return db_usuario
   
    @staticmethod
    def eliminar_asesor_completamente(db:Session, db_usaurio:Usuario):
        db.delete(db_usaurio)
        db.commit()