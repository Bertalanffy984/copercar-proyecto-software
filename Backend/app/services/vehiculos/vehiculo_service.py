from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.vehiculo.vehiculo_repository import VehiculoRepository
from app.schemas.BaseDB.vehiculo import VehiculoCreate, VehiculoUpdate

class VehiculoService:
    
    errores={
        "vehiculo_existe":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El vehiculo con esa placa ya existe (mirar en los carros inactivos si no se encuetra en los activos)"),
        "vehiculo_no_placa":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se encuentra un vehiculo con esa placa"),
        "error_id_vehiculo":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se encuentra un vehiculo con ese id"),
        "error_concurrencia_crear":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Conflicto de concurrencia: Este vehiculo acaba de ser registrado por otra solicitud simultanea"),
    }
    
    @staticmethod
    def crear_vehiculo(db:Session, vehiculo_a_ingresar:VehiculoCreate):
        if VehiculoRepository.obtener_vehiculo_placa_general(db=db, placa=vehiculo_a_ingresar.placa):
            raise VehiculoService.errores["vehiculo_existe"]
        try:
            return VehiculoRepository.crear_vehiculo(db=db,vehiculo_a_ingresar = vehiculo_a_ingresar)
        except IntegrityError:
            db.rollback()
            raise VehiculoService.errores["error_concurrencia_crear"]
        
        
    @staticmethod
    def buscar_por_placa(db:Session, placa:str):
        vehiculo_buscado=VehiculoRepository.obtener_vehiculo_activo_por_placa(db=db,placa=placa)
        if not vehiculo_buscado:
            raise VehiculoService.errores["vehiculo_no_placa"]
        return vehiculo_buscado
    
    @staticmethod
    def filtrar_vehiculo_por_estado(db:Session, id_estado:int):
        return VehiculoRepository.filtrar_por_estado(db=db, id_estado=id_estado)
    
    @staticmethod
    def listar_vehiculos_activos(db:Session, skip:int=0, limit:int=15):
        return VehiculoRepository.listar_vehiculos_activos(db=db, skip=skip, limit=limit)
    
    @staticmethod
    def actualizar_vehiculo(db:Session, id_vehiculo:int, vehiculo_actualizar:VehiculoUpdate):
        db_vehiculo=VehiculoRepository.obtener_vehiculo_por_id(db=db, id_vehiculo=id_vehiculo)
        if not db_vehiculo:
            raise VehiculoService.errores["error_id_vehiculo"]
        if vehiculo_actualizar.placa and vehiculo_actualizar.placa.upper() != db_vehiculo.placa:
            vehiculo_placa_igual=VehiculoRepository.obtener_vehiculo_placa_general(db=db,placa=vehiculo_actualizar.placa)
            if vehiculo_placa_igual:
                raise VehiculoService.errores["vehiculo_existe"]  
        return VehiculoRepository.editar_vehiculo(db=db, db_vehiculo = db_vehiculo, vehiculo_actualizar = vehiculo_actualizar)    
    
    @staticmethod
    def cambiar_estado_activo_vehiculo(db:Session, id_vehiculo:int):
        db_vehiculo=VehiculoRepository.obtener_vehiculo_por_id(db=db, id_vehiculo=id_vehiculo)
        if not db_vehiculo:
            raise VehiculoService.errores["error_id_vehiculo"]
        return VehiculoRepository.cambiar_estado_activo_vehiculo(db=db, db_vehiculo = db_vehiculo)