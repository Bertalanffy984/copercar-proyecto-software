from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.dependencies.rol_dependencies import obtener_administrador 
from app.schemas.schemas_db.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services.usuarios_services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios",tags=["Gestión de Usuarios (admin)"],dependencies=[Depends(obtener_administrador)])

@router.post("/crear/",response_model=UsuarioResponse,status_code=status.HTTP_201_CREATED,summary="Agregar nuevo usuario (Asesor)")
def agregar_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
  return UsuarioService.crear_usuario(db=db, usuario_in=usuario_in)

@router.get("/buscar/{numero_documento}",response_model=UsuarioResponse,status_code=status.HTTP_200_OK, summary="Buscar usuario por numero de documento (tener en cuenta que es un varchar)")
def buscar_usuario_por_documento(numero_documento: str, db: Session = Depends(get_db)):
  return UsuarioService.buscar_por_documento(db=db, numero_documento=numero_documento)

@router.get("/listar/",response_model=list[UsuarioResponse],status_code=status.HTTP_200_OK,summary="Listar usuarios (1.admin | 2.acesor)  id_rol=Null(todos los usuarios)")
def listar_usuarios_filtrar_rol(id_rol:int| None = None, skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
  return UsuarioService.listar_usuarios_filtrado(db=db,id_rol=id_rol, skip=skip, limit=limit)

@router.put("/modificar/{id_usuario}",response_model=UsuarioResponse,status_code=status.HTTP_200_OK, summary="Modificar información del usuario(asesor)")
def modificar_usuario(id_usuario: int, usuario_in: UsuarioUpdate, db: Session = Depends(get_db)):
  return UsuarioService.actualizar_usuario(
      db=db, id_usuario=id_usuario, usuario_in=usuario_in
  )

@router.delete("/elimiar/{id_usuario}", status_code=status.HTTP_200_OK, summary="Eliminar usuario de la BD")
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
  return UsuarioService.eliminar_usuario(db=db, id_usuario=id_usuario)