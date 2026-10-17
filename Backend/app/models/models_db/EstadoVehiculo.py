from ..base import *
class EstadoVehiculo(Base):
  __tablename__ = "estado_vehiculo"

  id_estado = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(30), unique=True, nullable=False)
  descripcion = Column(String(100), nullable=True)

  vehiculos = relationship("Vehiculo", back_populates="estado")