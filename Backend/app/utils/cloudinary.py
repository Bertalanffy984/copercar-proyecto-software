import cloudinary
import cloudinary.uploader
import os
from fastapi import HTTPException, status

error={"error_sub_img":HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al subir la imagen en la nube")}
def subir_imagen_cloudinary(imagen_bin:str)->str:
    try:
        respuesta=cloudinary.uploader.upload(imagen_bin, folder="copercar_vehiculos")
        return {
            "ruta": respuesta.get("secure_url"),
            "public_id": respuesta.get("public_id"),
    }
    except Exception as e:
        raise error["error_sub_img"]