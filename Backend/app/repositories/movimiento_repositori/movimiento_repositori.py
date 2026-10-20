from datetime import date
from sqlalchemy.orm import Session
from app.models.models_db.MovimientoVehiculo import MovimientoVehiculo
from app.schemas.BaseDB.movimiento import MovimientoCreate, MovimientoUpdate


class MovimientoRepository:

  @staticmethod
  def obtener_por_id(db: Session, id_movimiento: int) -> MovimientoVehiculo | None:
    return (
        db.query(MovimientoVehiculo)
        .filter(MovimientoVehiculo.id_movimiento == id_movimiento, MovimientoVehiculo.activo == True)
        .first()
    )

  @staticmethod
  def registrar(db: Session, movimiento_in: MovimientoCreate, id_usuario: int) -> MovimientoVehiculo:
    nuevo_movimiento = MovimientoVehiculo(**movimiento_in.model_dump(), id_usuario=id_usuario, activo=True)
    db.add(nuevo_movimiento)
    db.commit()
    db.refresh(nuevo_movimiento)
    return nuevo_movimiento

  @staticmethod
  def listar_filtrados(db: Session, placa: str | None = None, id_tipo_movimiento: int | None = None, fecha: date | None = None, skip: int = 0, limit: int = 50) -> list[MovimientoVehiculo]:
   
    query = db.query(MovimientoVehiculo).filter(MovimientoVehiculo.activo == True)
    if placa:
      query = query.join(MovimientoVehiculo.vehiculo).filter(MovimientoVehiculo.vehiculo.has(placa=placa))
      
    if id_tipo_movimiento:
      query = query.filter(MovimientoVehiculo.id_tipo_movimiento == id_tipo_movimiento)
    if fecha:
      query = query.filter(MovimientoVehiculo.fecha_movimiento == fecha)
      
    return query.offset(skip).limit(limit).all()

  @staticmethod
  def actualizar(db: Session, db_movimiento: MovimientoVehiculo, movimiento_in: MovimientoUpdate) -> MovimientoVehiculo:
    datos_actualizar = movimiento_in.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizar.items():
      setattr(db_movimiento, campo, valor)

    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento

  @staticmethod
  def cambiar_estado_activo_movimiento(db: Session, db_movimiento: MovimientoVehiculo) -> MovimientoVehiculo:
    db_movimiento.activo = False
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento