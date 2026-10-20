
from fastapi import UploadFile
from app.utils.errores_http import errores
from sqlalchemy.orm import Session
from app.repositories.vehiculo_repositori.foto_vehiculo_repository import FotoVehiculoRepository
from app.repositories.vehiculo_repositori.vehiculo_repository import VehiculoRepository
from app.schemas.BaseDB.foto_vehiculo import FotoVehiculoCreate
from app.utils.cloudinary import subir_imagen_cloudinary


class FotoVehiculoService:

  @staticmethod
  async def agregar_foto_a_vehiculo( db: Session, id_vehiculo: int, archivo: UploadFile, es_principal: bool, orden: int = 0):
    vehiculo = VehiculoRepository.obtener_vehiculo_por_id(db=db, id_vehiculo=id_vehiculo)
    if not vehiculo:
      raise errores["error_id_vehiculo"]

    if not archivo.content_type or not archivo.content_type.startswith("image/"):
      raise errores["error_formato"]
    
    es_principal = FotoVehiculoService.verificar_total_imagenes(db=db, id_vehiculo=id_vehiculo, es_principal=es_principal)
    
    contenido = await archivo.read()
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
          raise errores["error_existe_principal"]
    return es_principal