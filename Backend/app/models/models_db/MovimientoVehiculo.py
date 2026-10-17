from ..base import *

class MovimientoVehiculo(Base):
  __tablename__ = "movimiento_vehiculo"

  id_movimiento = Column(Integer, primary_key=True, autoincrement=True)
  id_vehiculo = Column(
      Integer, ForeignKey("vehiculo.id_vehiculo"), nullable=False
  )
  id_tipo_movimiento = Column(
      Integer, ForeignKey("tipo_movimiento.id_tipo_movimiento"), nullable=False
  )
  id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
  fecha_movimiento = Column(Date, nullable=False)
  valor = Column(Numeric(15, 2), nullable=False)
  observacion = Column(String(255), nullable=True)
  activo = Column(Boolean, nullable=False, default=True)

  vehiculo = relationship("Vehiculo", back_populates="movimientos")
  tipo_movimiento = relationship("TipoMovimiento", back_populates="movimientos")
  usuario = relationship("Usuario", back_populates="movimientos")

  __table_args__ = (
      CheckConstraint("valor > 0", name="ck_movimiento_valor"),
  )