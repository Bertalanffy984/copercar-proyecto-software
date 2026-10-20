from sqlalchemy.orm import Session
from app.models.models_db import Vehiculo 
from app.schemas.BaseDB.vehiculo import VehiculoCreate,VehiculoUpdate

class VehiculoRepository():
    @staticmethod
    def obtener_vehiculo_por_id(db:Session, id_vehiculo:int)->Vehiculo | None:
        return(
            db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo, Vehiculo.activo == True).first()
        )
        
    @staticmethod
    def obtener_vehiculo_activo_por_placa(db:Session, placa:str)->Vehiculo | None:
        return(
            db.query(Vehiculo).filter(Vehiculo.placa == placa.upper(), Vehiculo.activo == True).first()
        )
    @staticmethod
    def obtener_vehiculo_placa_general(db:Session, placa:str) -> Vehiculo | None:
        return (
        db.query(Vehiculo)
        .filter(Vehiculo.placa == placa.upper())
        .first()
    )
    
    @staticmethod
    def listar_vehiculos_activos(db:Session, skip:int=0, limit:int=15):
        return(
            db.query(Vehiculo).filter(Vehiculo.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
    @staticmethod
    def filtrar_por_estado(db:Session, id_estado:int)->Vehiculo:
        return(
            db.query(Vehiculo).filter(Vehiculo.id_estado == id_estado)
            .all()
        )
    @staticmethod
    
    def crear_vehiculo(db:Session, vehiculo_a_ingresar:VehiculoCreate)->Vehiculo:
        datos=vehiculo_a_ingresar.model_dump()
        datos["placa"]= datos["placa"].upper()
        
        db_vehiculo = Vehiculo(**datos)
        db.add(db_vehiculo)
        db.commit()
        db.refresh(db_vehiculo)
        return db_vehiculo
    
    @staticmethod
    def editar_vehiculo(db:Session, db_vehiculo:Vehiculo, vehiculo_actualizar:VehiculoUpdate)->Vehiculo:
        datos_edicion=vehiculo_actualizar.model_dump(exclude_unset=True, exclude_none=True)
        if "placa" in datos_edicion:
            datos_edicion["placa"]=datos_edicion["placa"].upper()
        for campo,valor in datos_edicion.items():
            setattr(db_vehiculo, campo,valor)
        db.commit()
        db.refresh(db_vehiculo)
        return db_vehiculo
    
    @staticmethod
    def cambiar_estado_activo_vehiculo(db:Session, db_vehiculo:Vehiculo)->Vehiculo:
        db_vehiculo.activo=False
        db.commit()
        return db_vehiculo