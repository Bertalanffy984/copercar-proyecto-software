from sqlalchemy.orm import Session
from app.models.models_db.Usuario import Usuario

class UsurioRepository:
    @staticmethod
    def get_por_correo(db:Session,correo:str)-> Usuario | None:
        return db.query(Usuario).filter(Usuario.correo == correo).first() 