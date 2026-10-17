from ..base import *
class Transmision(Base):
  __tablename__ = "transmision"

  id_transmision = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(30), unique=True, nullable=False)

  vehiculos = relationship("Vehiculo", back_populates="transmision")