from sqlalchemy.orm import Session
from app.repositories.marca_linea_repositories.marca_linea_repositories import MarcaLineaRepository
from app.schemas.schemas_db.marca import MarcaUpdate, MarcaResponse
from app.schemas.schemas_db.linea import LineaUpdate
from app.schemas.schemas_db.marca_linea import MarcaLineaTransaccionalCreate
from app.utils.respuestas_http_util import error_http

class MarcaLineaService:
    
    @staticmethod
    def crear_marca_linea(db:Session, marca_linea_in:MarcaLineaTransaccionalCreate)-> dict:
        marca=MarcaLineaRepository.obtener_marca_nombre(db=db, nombre=marca_linea_in.nombre_marca)
        if not marca:
          marca = MarcaLineaRepository.crear_marca(db=db, nombre=marca_linea_in.nombre_marca)
        elif not marca.activo:
          marca = MarcaLineaRepository.cambiar_estado_marca(db=db,marca=marca,)
        linea_existe=MarcaLineaRepository.obtener_linea_por_nombre_y_marca(db=db, id_marca=marca.id_marca, nombre_linea=marca_linea_in.nombre_linea)
        if linea_existe:
          if not linea_existe.activo:
            MarcaLineaRepository.cambiar_estado_linea(db=db,linea=linea_existe)
          else:
            raise error_http('linea_duplicada')
        else:
         MarcaLineaRepository.crear_linea(db=db, nombre_linea=marca_linea_in.nombre_linea, id_marca=marca.id_marca)
        return { "exito": f"200(OK): Línea '{marca_linea_in.nombre_linea}' asociada a marca '{marca_linea_in.nombre_marca}'"}
    
    @staticmethod
    def listar_catalogo(db:Session,skip: int = 0, limit: int = 25)->list[MarcaResponse]:
        return MarcaLineaRepository.listar_marcas_activas(db=db,skip=skip,limit=limit)
    
    @staticmethod
    def actualizar_marca(db: Session, id_marca: int, datos_update: MarcaUpdate) -> dict:
       marca = MarcaLineaRepository.obtener_marca_id(db=db, id_marca=id_marca)
       if not marca:
         raise error_http("marca_no_existe")
       
       marca_duplicada = MarcaLineaRepository.obtener_marca_nombre(db=db, nombre=datos_update.nombre)
       if marca_duplicada and marca_duplicada.id_marca != id_marca:
         raise error_http("marca_duplicada")

       marca.nombre = datos_update.nombre
       db.commit()
       return {"exito": "(200)OK, Marca actualizada correctamente."}

    @staticmethod
    def actualizar_linea(db: Session, id_linea: int, datos_update: LineaUpdate) -> dict:
       linea = MarcaLineaRepository.obtener_linea_id(db=db,id_linea=id_linea)
       if not linea:
         raise error_http("linea_no_existe")

       if datos_update.id_marca is not None and datos_update.id_marca != linea.id_marca:
         nueva_marca = MarcaLineaRepository.obtener_marca_id(db, datos_update.id_marca)
         if not nueva_marca:
           raise error_http("marca_no_existe")
         linea.id_marca = datos_update.id_marca

       if datos_update.nombre is not None:
         linea.nombre = datos_update.nombre

       db.commit()
       return {"detail": "Línea actualizada correctamente."}
     
    @staticmethod
    def eliminar_marca(db:Session, id_marca:int)->dict:
      marca = MarcaLineaRepository.obtener_marca_id(db=db,id_marca=id_marca)
      if not marca or not marca.activo:
        raise error_http("marca_no_existe")
      
      MarcaLineaRepository.eliminar_marca_logica_cascada(db=db,marca=marca)
      return {"exito": "200(OK), la marca junto con sus lineas ha sido eliminado de las listas."}

    @staticmethod
    def eliminar_linea(db: Session, id_linea: int) -> dict:
       linea = MarcaLineaRepository.obtener_linea_id(db=db, id_linea=id_linea)
       if not linea or not linea.activo:
         raise error_http("linea_no_existe")

       MarcaLineaRepository.cambiar_estado_linea(db=db, linea=linea)
       return {"exito": "(200) OK, línea eliminada correctamente de las listas."}
    