import cloudinary
import cloudinary.uploader
from app.utils.respuestas_http_util import error_http

def subir_imagen_cloudinary(imagen_bin: bytes) -> dict[str, str | None]:
    try:
        respuesta = cloudinary.uploader.upload(
            imagen_bin,
            folder="copercar_vehiculos",
            timeout=30,
        )
        return {
            "ruta": respuesta.get("secure_url"),
            "public_id": respuesta.get("public_id"),
        }
    except Exception as e:
        raise error_http("error_sub_nube") from e

def eliminar_imagen_cloudinary(public_id:str) -> dict:
    try:
        respuesta=cloudinary.uploader.destroy(public_id=public_id)
        if respuesta.get('result') not in ["ok", "not found"]:
            raise error_http("error_eliminar_de_nube")
    except Exception as e:
        raise error_http('error_eliminar_de_nube') from e