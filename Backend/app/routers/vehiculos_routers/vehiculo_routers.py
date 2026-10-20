from typing import List, Annotated
from fastapi import APIRouter,Query, Depends, status,UploadFile,File
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.schemas.BaseDB.vehiculo import (VehiculoCreate, VehiculoUpdate, VehiculoResponse,FotoVehiculoResponse)
from app.services.vehiculos.vehiculo_service import VehiculoService
from app.services.vehiculos.vehiculo_foto_service import FotoVehiculoService
from app.dependencies.jwt_dependecia import obtener_usuario_activo

router = APIRouter( prefix="/vehiculos", tags=["Vehículos (Inventario)"], dependencies=[Depends(obtener_usuario_activo)])


@router.post("/crear", response_model=VehiculoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_vehiculo(vehiculo_in: VehiculoCreate, db: Session = Depends(get_db)):
  return VehiculoService.crear_vehiculo(db, vehiculo_in)

@router.get("/listar_activos", response_model=List[VehiculoResponse], status_code=status.HTTP_200_OK)
async def listar_vehiculos_activos(
  skip:Annotated[int, Query(ge=0, description="Número de registros a omitir")] = 0,
  limit: Annotated[int, Query(ge=1, le=20, description="Cantidad máxima de registros por página")] = 20,
  db: Session = Depends(get_db)):
  
  return VehiculoService.listar_vehiculos_activos(db=db, skip=skip, limit=limit)


@router.get("/placa/{placa}", response_model=VehiculoResponse, status_code=status.HTTP_200_OK)
async def buscar_vehiculo_por_placa(placa: str, db: Session = Depends(get_db)):
  return VehiculoService.buscar_por_placa(db, placa)


@router.get("/filtrar/estado/{id_estado}", response_model=List[VehiculoResponse],status_code=status.HTTP_200_OK)
async def filtrar_vehiculos_estado(id_estado: int, db: Session = Depends(get_db)):
  return VehiculoService.filtrar_vehiculo_por_estado(db, id_estado)


@router.put("/actualizar/{id_vehiculo}", response_model=VehiculoResponse)
async def actualizar_vehiculo(id_vehiculo: int, vehiculo_in: VehiculoUpdate, db: Session = Depends(get_db),):
  return VehiculoService.actualizar_vehiculo(db, id_vehiculo, vehiculo_in)


@router.delete("/eliminar/{id_vehiculo}", status_code=status.HTTP_200_OK)
#este endpoint no elimina de la base de datos, solo cambia el estado activo que define si mostrar o no el carro.
async def eliminar_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
  VehiculoService.cambiar_estado_activo_vehiculo(db = db, id_vehiculo = id_vehiculo)
  return {
      "mensaje": f"El estado ha cambiado correctamente",
  }

@router.post("/subir_foto/{id_vehiculo}/", response_model=FotoVehiculoResponse, status_code=status.HTTP_201_CREATED)
async def subir_foto_vehiculo(id_vehiculo: int,
    db: Session = Depends(get_db),
    archivo: UploadFile = File(...),
    es_principal: bool = Query(False),
    orden: int = Query(0, ge=0),
):
  return await FotoVehiculoService.agregar_foto_a_vehiculo(
      db=db,
      id_vehiculo=id_vehiculo,
      archivo=archivo,
      es_principal=es_principal,
      orden=orden,
  )