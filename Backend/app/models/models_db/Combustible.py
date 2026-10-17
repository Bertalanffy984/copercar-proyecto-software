from ..base import *

class Combustible(Base):
  __tablename__ = "combustible"

  id_combustible = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(30), unique=True, nullable=False)

  vehiculos = relationship("Vehiculo", back_populates="combustible")