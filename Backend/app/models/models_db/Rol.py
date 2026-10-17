from ..base import *

class Rol(Base):
  __tablename__ = "rol"

  id_rol = Column(Integer, primary_key=True, autoincrement=True)
  nombre_rol = Column(String(30), unique=True, nullable=False)
  descripcion = Column(String(100), nullable=True)

  usuarios = relationship("Usuario", back_populates="rol")