from ..base import *
class Marca(Base):
  __tablename__ = "marca"

  id_marca = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(50), unique=True, nullable=False)

  lineas = relationship("Linea", back_populates="marca")