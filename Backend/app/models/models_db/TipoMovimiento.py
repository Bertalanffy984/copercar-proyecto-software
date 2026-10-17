from ..base import *

class TipoMovimiento(Base):
  __tablename__ = "tipo_movimiento"

  id_tipo_movimiento = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(40), unique=True, nullable=False)
  naturaleza = Column(Enum("INGRESO", "EGRESO"), nullable=False)
  descripcion = Column(String(100), nullable=True)

  movimientos = relationship("MovimientoVehiculo", back_populates="tipo_movimiento")