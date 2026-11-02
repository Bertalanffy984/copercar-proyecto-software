
from fastapi import UploadFile
from app.utils.respuestas_http_util import error_http
from sqlalchemy.orm import Session
from app.repositories.vehiculos_repositories.foto_vehiculo_repositori import FotoVehiculoRepository
from app.repositories.vehiculos_repositories.vehiculo_repositori import VehiculoRepository
from app.schemas.schemas_db.foto_vehiculo import FotoVehiculoCreate
from app.utils.cloudinary_util import subir_imagen_cloudinary,eliminar_imagen_cloudinary

MAX_FOTO_SIZE_BYTES = 10 * 1024 * 1024


class FotoVehiculoService:

  @staticmethod
  def agregar_foto_a_vehiculo( db: Session, id_vehiculo: int, archivo: UploadFile, es_principal: bool, orden: int = 0):
    vehiculo = VehiculoRepository.obtener_vehiculo_por_id(db=db, id_vehiculo=id_vehiculo)
    if not vehiculo:
      raise error_http("error_id_vehiculo")
    
    contenido = archivo.file.read(MAX_FOTO_SIZE_BYTES + 1)
    if len(contenido) > MAX_FOTO_SIZE_BYTES:
      raise error_http("foto_supera_tamano_maximo")

    es_principal = FotoVehiculoService.verificar_total_imagenes(db=db, id_vehiculo=id_vehiculo, es_principal=es_principal)
    datos_nube = subir_imagen_cloudinary(contenido)
    foto_dto = FotoVehiculoCreate(
        id_vehiculo=id_vehiculo,
        ruta=datos_nube["ruta"],
        public_id=datos_nube["public_id"],
        es_principal=es_principal,
        orden=orden,
    )
    return FotoVehiculoRepository.registrar_foto(db=db, foto_in=foto_dto)

  def verificar_total_imagenes(db: Session, id_vehiculo: int, es_principal: bool):
    total_fotos=FotoVehiculoRepository.contar_fotos_vehiculo(db=db, id_vehiculo=id_vehiculo)
    if total_fotos==0:
      return True
    else:
      if es_principal:
        foto_principal_actual = FotoVehiculoRepository.obtener_foto_principal(db, id_vehiculo)
        if foto_principal_actual:
          raise error_http("error_existe_principal")
    return es_principal

  @staticmethod
  def eliminar_fotografia(db: Session, id_fotografia: int) -> dict:
    foto = FotoVehiculoRepository.obtener_por_id(db, id_fotografia)
    if not foto:
      raise error_http("fotografia_no_existe")
    public_id = foto.public_id 
    era_principal = foto.es_principal
    id_vehiculo_actual = foto.id_vehiculo
    
    eliminar_imagen_cloudinary(public_id)
    FotoVehiculoRepository.eliminar_fisica(db=db,db_fotografia = foto)
    
    FotoVehiculoService.reasignar_principal(era_principal, id_vehiculo_actual, db)
    
    return {'exito':'200(OK), la foto fue eliminada correctamente'} 
  
  def reasignar_principal(era_principal:bool, id_vehiculo_actual:int, db:Session):
    if era_principal:
      siguiente_foto=FotoVehiculoRepository.obtener_siguiente_foto_disponible(db, id_vehiculo_actual)
      if siguiente_foto:
        FotoVehiculoRepository.asignar_como_principal(db, siguiente_foto)
       