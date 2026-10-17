from ..base import *

class FotoVehiculo(Base):
  __tablename__ = "foto_vehiculo"

  id_foto = Column(Integer, primary_key=True, autoincrement=True)
  id_vehiculo = Column(
      Integer, ForeignKey("vehiculo.id_vehiculo"), nullable=False
  )
  ruta = Column(String(2048), nullable=False)
  public_id = Column(String(255), unique=True, nullable=False)
  es_principal = Column(Boolean, nullable=False, default=False)
  orden = Column(Integer, nullable=False, default=0)

  vehiculo = relationship("Vehiculo", back_populates="fotos")

  __table_args__ = (
      CheckConstraint("orden >= 0", name="ck_foto_orden"),
  )