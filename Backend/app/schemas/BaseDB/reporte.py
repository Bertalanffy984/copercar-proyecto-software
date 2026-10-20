from datetime import date
from decimal import Decimal
from app.schemas.base import ConConfigBaseModel


class DetalleVehiculoReporte(ConConfigBaseModel):
  placa: str
  vehiculo: str  # Título o nombre del vehículo
  fecha: date
  valor: Decimal


class ReporteMensualResponse(ConConfigBaseModel):
  anio: int
  mes: int
  ingresos_totales: Decimal
  egresos_totales: Decimal
  ganancia_neta: Decimal
  cantidad_movimientos: int
  vehiculos_comprados: list[DetalleVehiculoReporte]
  vehiculos_vendidos: list[DetalleVehiculoReporte]