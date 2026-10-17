from ..base import *
class Usuario(Base):
  __tablename__ = "usuario"

  id_usuario = Column(Integer, primary_key=True, autoincrement=True)
  id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)
  tipo_documento = Column(String(4), nullable=False)
  numero_documento = Column(String(20), nullable=False)
  primer_nombre = Column(String(50), nullable=False)
  segundo_nombre = Column(String(50), nullable=True)
  primer_apellido = Column(String(50), nullable=False)
  segundo_apellido = Column(String(50), nullable=True)
  correo = Column(String(100), unique=True, nullable=False)
  celular = Column(String(20), nullable=False)
  fecha_nacimiento = Column(Date, nullable=False)
  genero = Column(String(20), nullable=False)
  direccion = Column(String(150), nullable=False)
  contrasena = Column(String(255), nullable=False)
  activo = Column(Boolean, nullable=False, default=False)
  fecha_registro = Column(DateTime, nullable=False, default=datetime.utcnow)

  rol = relationship("Rol", back_populates="usuarios")
  movimientos = relationship("MovimientoVehiculo", back_populates="usuario")

  __table_args__ = (
      UniqueConstraint(
          "tipo_documento", "numero_documento", name="uq_usuario_documento"
      ),
  )