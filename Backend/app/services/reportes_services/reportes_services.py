from decimal import Decimal
from sqlalchemy.orm import Session
from app.repositories.reportes_repositories.reportes_repositories import ReporteRepository 
from app.schemas.BaseDB.reporte import (DetalleVehiculoReporte, ReporteMensualResponse)

class ReporteService:
    
    @staticmethod
    def generar_reporte_mensual(db:Session, anio:int, mes:int) -> ReporteMensualResponse:
        movimientos=ReporteRepository.obtener_movimiento_por_periodo(db=db, anio=anio, mes=mes)
        
        ingresos_totales = Decimal("0.00")
        egresos_totales = Decimal("0.00")
        vehiculos_comprados: list[DetalleVehiculoReporte] = []
        vehiculos_vendidos: list[DetalleVehiculoReporte] = []
        
        for mov in movimientos:
            detalle = DetalleVehiculoReporte(
            placa=mov.vehiculo.placa,
            vehiculo=mov.vehiculo.titulo,
            fecha=mov.fecha_movimiento,
            valor=mov.valor
            )
            print(f"MIRAR AQUIoajikhdopiashdophanos[fhnaipusfbguioasbfo[iasfniu]] {mov.id_movimiento}")

            if "INGRESO" in mov.tipo_movimiento.naturaleza:
                ingresos_totales+=mov.valor
            elif "EGRESO" in mov.tipo_movimiento.naturaleza:
                egresos_totales+=mov.valor
                
            if "COMPRA" in mov.tipo_movimiento.nombre:
                vehiculos_comprados.append(detalle)
            elif "VENTA" in mov.tipo_movimiento.nombre:
                vehiculos_vendidos.append(detalle)
        
        ganancia_neta=ingresos_totales - egresos_totales
        
        return ReporteMensualResponse(
            anio=anio,
            mes=mes,
            ingresos_totales=ingresos_totales,
            egresos_totales=egresos_totales,
            ganancia_neta=ganancia_neta,
            cantidad_movimientos=len(movimientos),
            vehiculos_comprados=vehiculos_comprados,
            vehiculos_vendidos=vehiculos_vendidos
        )