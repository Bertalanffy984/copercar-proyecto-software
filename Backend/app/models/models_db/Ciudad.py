from ..base import *
class Ciudad(Base):
  __tablename__ = "ciudad"

  id_ciudad = Column(Integer, primary_key=True, autoincrement=True)
  id_departamento = Column(
      Integer, ForeignKey("departamento.id_departamento"), nullable=False
  )
  nombre = Column(String(50), nullable=False)

  departamento = relationship("Departamento", back_populates="ciudades")
  vehiculos = relationship("Vehiculo", back_populates="ciudad")

  __table_args__ = (
      UniqueConstraint(
          "id_departamento", "nombre", name="uq_ciudad_departamento_nombre"
      ),
  )