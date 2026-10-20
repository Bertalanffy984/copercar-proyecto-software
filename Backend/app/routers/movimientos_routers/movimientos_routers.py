from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.dependencies.rol_dependencies import obtener_administrador 
from app.models.models_db.Usuario import Usuario
from app.schemas.BaseDB.movimiento import (MovimientoCreate,MovimientoResponse,MovimientoUpdate)
from app.services.movimientos.movimientos_services import MovimientoService

router = APIRouter(prefix="/movimientos",tags=["Gestión de Movimientos (admin)"],dependencies=[Depends(obtener_administrador)],)


@router.post("/crear",response_model=MovimientoResponse,status_code=status.HTTP_201_CREATED,summary="Registrar movimiento de vehículo",)
def registrar_movimiento( movimiento_in: MovimientoCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(obtener_administrador)):
  return MovimientoService.registrar_movimiento(db=db, movimiento_in=movimiento_in, id_usuario_actual=usuario_actual.id_usuario)


@router.get("/filtrar", response_model=list[MovimientoResponse], status_code=status.HTTP_200_OK, summary="Consultar y filtrar movimientos de vehículos")
def consultar_movimientos(
    placa: str | None = Query(None),
    id_tipo_movimiento: int | None = Query(None),
    fecha: date | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
  return MovimientoService.consultar_movimientos(db=db, placa=placa, id_tipo_movimiento=id_tipo_movimiento, fecha=fecha, skip=skip, limit=limit)


@router.put("/actualizar/{id_movimiento}", response_model=MovimientoResponse, status_code=status.HTTP_200_OK, summary="Modificar movimiento de vehículo")
def modificar_movimiento(id_movimiento: int, movimiento_in: MovimientoUpdate, db: Session = Depends(get_db)):
  return MovimientoService.modificar_movimiento(db=db, id_movimiento=id_movimiento, movimiento_in=movimiento_in)


@router.delete("/eliminar/{id_movimiento}", status_code=status.HTTP_200_OK, summary="RFE-14: Eliminar lógicamente un movimiento")
def eliminar_movimiento(id_movimiento: int, db: Session = Depends(get_db)):
  return MovimientoService.eliminar_movimiento(db=db, id_movimiento=id_movimiento)