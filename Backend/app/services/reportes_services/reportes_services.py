from decimal import Decimal
from sqlalchemy.orm import Session
from app.repositories.reportes_repositories.reportes_repositories import ReporteRepository 
from app.schemas.schemas_db.reporte import (DetalleVehiculoReporte, ReporteMensualResponse, DetalleVehiculoRegistrado)

class ReporteService:
    
    @staticmethod
    def _procesar_movimientos_financieros(movimientos:list) -> tuple:
        ingresos_totales = Decimal("0.00")
        egresos_totales = Decimal("0.00")
        vehiculos_comprados: list[DetalleVehiculoReporte] = []
        vehiculos_vendidos: list[DetalleVehiculoReporte] = []
        
        for mov in movimientos:
            if not mov.vehiculo or not mov.tipo_movimiento:
                continue
            detalle = DetalleVehiculoReporte(
            placa=mov.vehiculo.placa,
            vehiculo=mov.vehiculo.titulo,
            fecha=mov.fecha_movimiento,
            valor=mov.valor
            )

            if "INGRESO" in mov.tipo_movimiento.naturaleza:
                ingresos_totales+=mov.valor
            elif "EGRESO" in mov.tipo_movimiento.naturaleza:
                egresos_totales+=mov.valor
                
            if "COMPRA" in mov.tipo_movimiento.nombre:
                vehiculos_comprados.append(detalle)
            elif "VENTA" in mov.tipo_movimiento.nombre:
                vehiculos_vendidos.append(detalle)
                
        return ingresos_totales, egresos_totales, vehiculos_comprados, vehiculos_vendidos
        
        
    @staticmethod
    def _procesar_vehiculos_registrados(vehiculos_mes: list) -> list[DetalleVehiculoRegistrado]:
        vehiculos_registrados: list[DetalleVehiculoRegistrado] = []
        for vehiculo in vehiculos_mes:
            estado_texto = "ACTIVO" if vehiculo.activo else "INACTIVO"
            detalle_reg = DetalleVehiculoRegistrado(
                placa=vehiculo.placa,
                vehiculo=vehiculo.titulo,
                fecha_registro=vehiculo.fecha_registro.date(),
                estado_actual=estado_texto
            )
            vehiculos_registrados.append(detalle_reg)
            
        return vehiculos_registrados
    
    @staticmethod
    def generar_reporte_mensual(db: Session, anio: int, mes: int) -> ReporteMensualResponse:
        movimientos = ReporteRepository.obtener_movimiento_por_periodo(db=db, anio=anio, mes=mes)
        vehiculos_mes = ReporteRepository.obtener_vehiculos_por_fecha_registro(db=db, anio=anio, mes=mes)
        
        ingresos, egresos, comprados, vendidos = ReporteService._procesar_movimientos_financieros(movimientos)
        registrados = ReporteService._procesar_vehiculos_registrados(vehiculos_mes)
        
        return ReporteMensualResponse(
            anio=anio,
            mes=mes,
            ingresos_totales=ingresos,
            egresos_totales=egresos,
            ganancia_neta=ingresos - egresos,
            cantidad_movimientos=len(movimientos),
            vehiculos_comprados=comprados,
            vehiculos_vendidos=vendidos,
            vehiculos_registrados=registrados
        )