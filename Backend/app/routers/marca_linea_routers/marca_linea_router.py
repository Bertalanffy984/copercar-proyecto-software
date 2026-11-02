from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.dependencies.rol_dependencies import obtener_administrador
from app.schemas.schemas_db.marca import MarcaUpdate, MarcaResponse
from app.schemas.schemas_db.linea import LineaUpdate
from app.schemas.schemas_db.marca_linea import MarcaLineaTransaccionalCreate
from app.services.marca_linea_services.marca_linea_service import MarcaLineaService

router = APIRouter(prefix="/marcas_lineas",tags=["Gestion de Marcas y Líneas para el (Admin)"],dependencies=[Depends(obtener_administrador)])

@router.post("/crear", status_code=status.HTTP_201_CREATED, summary="Crear Marca y Línea en un solo paso")
def crear_marca_y_linea(marca_linea_in: MarcaLineaTransaccionalCreate, db: Session = Depends(get_db)):
  return MarcaLineaService.crear_marca_linea(db=db, marca_linea_in=marca_linea_in)

@router.get("/listar/", response_model=list[MarcaResponse], status_code=status.HTTP_200_OK, summary="Listar Marcas con sus Líneas")
def listar_catalogo(db: Session = Depends(get_db), skip:int=Query(0,ge=0), limit:int=Query(25, ge=1, le=100)):
  return MarcaLineaService.listar_catalogo(db,skip,limit)

@router.put("/actualizar/marcas/{id_marca}", status_code=status.HTTP_200_OK, summary="Actualizar nombre de Marca")
def actualizar_marca(id_marca: int, datos_update: MarcaUpdate, db: Session = Depends(get_db)):
  return MarcaLineaService.actualizar_marca(db, id_marca, datos_update)

@router.put("/actualizar/lineas/{id_linea}", status_code=status.HTTP_200_OK, summary="Actualizar o reasignar Línea")
def actualizar_linea(id_linea: int, datos_update: LineaUpdate, db: Session = Depends(get_db)):
  return MarcaLineaService.actualizar_linea(db, id_linea, datos_update)

@router.delete("/eliminar/marca/{id_marca}",status_code=status.HTTP_200_OK, summary="Eliminar marca de forma recuperable")
def eliminar_marca(id_marca:int, db: Session = Depends(get_db)):
  return MarcaLineaService.eliminar_marca(db=db, id_marca=id_marca)

@router.delete("/eliminar/linea/{id_linea}", status_code=status.HTTP_200_OK, summary="Eliminar Línea de forma recuperable")
def eliminar_linea(id_linea: int, db: Session = Depends(get_db)):
  return MarcaLineaService.eliminar_linea(db, id_linea)