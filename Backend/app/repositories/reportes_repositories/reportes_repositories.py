from sqlalchemy import extract
from sqlalchemy.orm import Session,joinedload
from app.models.models_db.MovimientoVehiculo import MovimientoVehiculo
from app.models.models_db.Vehiculo import Vehiculo

class ReporteRepository:
    
    @staticmethod
    def obtener_movimiento_por_periodo(db: Session, anio: int, mes: int) -> list[MovimientoVehiculo]:
        return (
            db.query(MovimientoVehiculo)
            .options(joinedload(MovimientoVehiculo.vehiculo),joinedload(MovimientoVehiculo.tipo_movimiento))
            .filter(
                MovimientoVehiculo.activo == True,
                extract("year", MovimientoVehiculo.fecha_movimiento) == anio,
                extract("month", MovimientoVehiculo.fecha_movimiento) == mes
            ).all()
        )
        
    @staticmethod
    def obtener_vehiculos_por_fecha_registro(db: Session, anio: int, mes: int) -> list[Vehiculo]:
        return (
            db.query(Vehiculo)
            .filter(
                extract("year", Vehiculo.fecha_registro) == anio,
                extract("month", Vehiculo.fecha_registro) == mes
            ).all()
        )