from ..base import *
class Linea(Base):
  __tablename__ = "linea"

  id_linea = Column(Integer, primary_key=True, autoincrement=True)
  id_marca = Column(Integer, ForeignKey("marca.id_marca"), nullable=False)
  nombre = Column(String(50), nullable=False)

  marca = relationship("Marca", back_populates="lineas")
  vehiculos = relationship("Vehiculo", back_populates="linea")

  __table_args__ = (
      UniqueConstraint("id_marca", "nombre", name="uq_linea_marca_nombre"),
  )