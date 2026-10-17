from ..base import *

class Departamento(Base):
  __tablename__ = "departamento"

  id_departamento = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(50), unique=True, nullable=False)

  ciudades = relationship("Ciudad", back_populates="departamento")