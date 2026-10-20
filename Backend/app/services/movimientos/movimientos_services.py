from datetime import date
from app.utils.errores_http import errores
from sqlalchemy.orm import Session
from app.repositories.movimiento_repositori.movimiento_repositori import MovimientoRepository
from app.repositories.vehiculo_repositori.vehiculo_repository import VehiculoRepository
from app.schemas.BaseDB.movimiento import ( MovimientoCreate, MovimientoResponse, MovimientoUpdate,)

class MovimientoService:

  @staticmethod
  def registrar_movimiento(db: Session, movimiento_in: MovimientoCreate, id_usuario_actual: int) -> MovimientoResponse:
    vehiculo = VehiculoRepository.obtener_vehiculo_por_id(db, movimiento_in.id_vehiculo)
    if not vehiculo:
      raise errores["no_hay_movimiento"]

    if movimiento_in.valor <= 0:
      raise errores["valor_nulo"]

    return MovimientoRepository.registrar(db=db, movimiento_in=movimiento_in, id_usuario=id_usuario_actual)

  @staticmethod
  def consultar_movimientos( db: Session, placa: str | None = None, id_tipo_movimiento: int | None = None, fecha: date | None = None, skip: int = 0, limit: int = 50) -> list[MovimientoResponse]:
    movimientos = MovimientoRepository.listar_filtrados(
        db=db,
        placa=placa,
        id_tipo_movimiento=id_tipo_movimiento,
        fecha=fecha,
        skip=skip,
        limit=limit,
    )
    print("Cantidad movimientos:", len(movimientos))
    if not movimientos and (placa or id_tipo_movimiento or fecha):
      raise errores["sin_resultados_filtrado"]
    return movimientos

  @staticmethod
  def modificar_movimiento(db: Session, id_movimiento: int, movimiento_in: MovimientoUpdate) -> MovimientoResponse:
    movimiento_existente = MovimientoRepository.obtener_por_id(db, id_movimiento)
    if not movimiento_existente:
      raise errores["sin_movimiento"]

    if movimiento_in.valor is not None and movimiento_in.valor <= 0:
      raise errores["valor_nulo"]

    return MovimientoRepository.actualizar(db=db, db_movimiento=movimiento_existente, movimiento_in=movimiento_in)

  @staticmethod
  def eliminar_movimiento(db: Session, id_movimiento: int) -> dict:
    movimiento_existente = MovimientoRepository.obtener_por_id(db, id_movimiento)
    if not movimiento_existente:
      raise errores["error_eliminar"]
  
    MovimientoRepository.cambiar_estado_activo_movimiento(db, movimiento_existente)
    return {"detail": "Operación exitosa. El estado de este movimiento cambio correctamente"}