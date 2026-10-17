from ..base import *
class Vehiculo(Base):
  __tablename__ = "vehiculo"

  id_vehiculo = Column(Integer, primary_key=True, autoincrement=True)
  id_linea = Column(Integer, ForeignKey("linea.id_linea"), nullable=False)
  id_estado = Column(
      Integer, ForeignKey("estado_vehiculo.id_estado"), nullable=False
  )
  id_ciudad = Column(Integer, ForeignKey("ciudad.id_ciudad"), nullable=False)
  titulo = Column(String(160), nullable=False)
  placa = Column(String(20), unique=True, nullable=False)
  color = Column(String(30), nullable=False)
  modelo = Column(Integer, nullable=False)
  kilometraje = Column(Integer, nullable=False, default=0)
  precio = Column(Numeric(15, 2), nullable=False)
  cantidad_duenos = Column(Integer, nullable=False, default=0)
  cilindraje = Column(Integer, nullable=True)
  id_combustible = Column(
      Integer, ForeignKey("combustible.id_combustible"), nullable=False
  )
  id_transmision = Column(
      Integer, ForeignKey("transmision.id_transmision"), nullable=False
  )
  fecha_vencimiento_soat = Column(Date, nullable=True)
  fecha_vencimiento_rtm = Column(Date, nullable=True)
  activo = Column(Boolean, nullable=False, default=True)
  fecha_registro = Column(DateTime, nullable=False, default=datetime.utcnow)

  linea = relationship("Linea", back_populates="vehiculos")
  estado = relationship("EstadoVehiculo", back_populates="vehiculos")
  ciudad = relationship("Ciudad", back_populates="vehiculos")
  combustible = relationship("Combustible", back_populates="vehiculos")
  transmision = relationship("Transmision", back_populates="vehiculos")
  fotos = relationship("FotoVehiculo", back_populates="vehiculo")
  movimientos = relationship("MovimientoVehiculo", back_populates="vehiculo")

  __table_args__ = (
      CheckConstraint("cilindraje >= 0 OR cilindraje IS NULL", name="ck_vehiculo_cilindraje"),
      CheckConstraint("cantidad_duenos >= 0", name="ck_vehiculo_duenos"),
      CheckConstraint("kilometraje >= 0", name="ck_vehiculo_km"),
      CheckConstraint("modelo BETWEEN 1900 AND 2100", name="ck_vehiculo_modelo"),
      CheckConstraint("precio > 0", name="ck_vehiculo_precio"),
  )