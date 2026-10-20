from sqlalchemy.orm import Session
from app.models.models_db.FotoVehiculo import FotoVehiculo
from app.schemas.BaseDB.foto_vehiculo import FotoVehiculoCreate

class FotoVehiculoRepository:
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