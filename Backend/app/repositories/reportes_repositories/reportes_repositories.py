from sqlalchemy import extract
from sqlalchemy.orm import Session
from app.models.models_db.MovimientoVehiculo import MovimientoVehiculo

class ReporteRepository:
    
    @staticmethod
    def obtener_movimiento_por_periodo(db:Session, anio:int, mes:int)->list[MovimientoVehiculo]:
        return(
            db.query(MovimientoVehiculo)
            .filter(MovimientoVehiculo.activo==True,
                    extract("year",MovimientoVehiculo.fecha_movimiento)==anio,
                    extract("month",MovimientoVehiculo.fecha_movimiento)==mes
            ).all())
    