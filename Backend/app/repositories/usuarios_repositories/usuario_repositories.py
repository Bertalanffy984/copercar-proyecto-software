from sqlalchemy.orm import Session
from app.models.models_db.Usuario import Usuario
from sqlalchemy.orm import Session
from app.models.models_db.Usuario import Usuario
from app.schemas.schemas_db.usuario import UsuarioCreate, UsuarioUpdate

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
    def listar_todos_usuarios_filtrado(db:Session, id_rol:int | None, skip:int=0, limit:int = 20)->list[Usuario]:
        query=db.query(Usuario)
        if id_rol is not None: query=query.filter(Usuario.id_rol==id_rol)
        return query.order_by(Usuario.id_rol.asc()).offset(skip).limit(limit).all()
        
    @staticmethod
    def crear_usuario(db: Session, usuario_in: UsuarioCreate, hash_pwd: str) -> Usuario:
        datos_dict=usuario_in.model_dump()
        datos_dict.pop("contrasena", None)
        nuevo_user=Usuario(
            **datos_dict,
            contrasena=hash_pwd,
            activo=True
        )
        db.add(nuevo_user)
        db.commit()
        db.refresh(nuevo_user)
        return nuevo_user
    
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
    def desactivar_usuario(db:Session, db_usuario:Usuario):
        db_usuario.activo=False
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    @staticmethod
    def activar_usuario(db:Session, db_usuario:Usuario):
        db_usuario.activo=True
        db.commit()
        db.refresh(db_usuario)
        return db_usuario