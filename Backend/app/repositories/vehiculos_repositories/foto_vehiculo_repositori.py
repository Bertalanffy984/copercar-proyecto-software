from sqlalchemy.orm import Session
from app.models.models_db.FotoVehiculo import FotoVehiculo
from app.schemas.schemas_db.foto_vehiculo import FotoVehiculoCreate

class FotoVehiculoRepository:
    
    @staticmethod
    def obtener_por_id(db: Session, id_fotografia: int) -> FotoVehiculo | None:
      return db.query(FotoVehiculo).filter(FotoVehiculo.id_foto == id_fotografia).first()
    
    @staticmethod
    def contar_fotos_vehiculo(db:Session, id_vehiculo:int)->int:
       return(db.query(FotoVehiculo)
              .filter(FotoVehiculo.id_vehiculo==id_vehiculo)
              .count())
    
    @staticmethod
    def obtener_foto_principal(db:Session, id_vehiculo:int) -> FotoVehiculo | None:
        return(
            db.query(FotoVehiculo)
            .filter(FotoVehiculo.id_vehiculo==id_vehiculo,FotoVehiculo.es_principal==True)
            .first()
        )
        
    @staticmethod
    def registrar_foto(db:Session, foto_in:FotoVehiculoCreate, )->FotoVehiculo:
        nueva_foto=FotoVehiculo(**foto_in.model_dump())
        db.add(nueva_foto)
        db.commit()
        db.refresh(nueva_foto)
        return nueva_foto
    
    @staticmethod
    def eliminar_fisica(db: Session, db_fotografia: FotoVehiculo) -> None:
     db.delete(db_fotografia)
     db.commit()
     
    @staticmethod
    def obtener_siguiente_foto_disponible(db: Session, id_vehiculo: int) -> FotoVehiculo | None:
      return (
        db.query(FotoVehiculo)
        .filter(FotoVehiculo.id_vehiculo == id_vehiculo)
        .order_by(FotoVehiculo.orden.asc(), FotoVehiculo.id_foto.asc())
        .first()
     )

    @staticmethod
    def asignar_como_principal(db: Session, db_fotografia: FotoVehiculo) -> None:
      db_fotografia.es_principal = True
      db.commit()
      db.refresh(db_fotografia)