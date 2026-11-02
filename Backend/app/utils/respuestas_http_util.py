from fastapi import HTTPException, status

_ERRORES_CATALOGO = {
    
    # --- Errores de Vehículos ---
    "vehiculo_existe": (status.HTTP_400_BAD_REQUEST,"El vehículo con esa placa ya existe (revisar en los vehículos inactivos si no se encuentra en los activos)",),
    "vehiculo_no_placa": (status.HTTP_404_NOT_FOUND, "No se encuentra un vehículo con esa placa"),
    "error_id_vehiculo": (status.HTTP_404_NOT_FOUND,"No se encuentra un vehículo con ese ID"),
    "error_concurrencia_crear": (status.HTTP_409_CONFLICT,"Conflicto de concurrencia: Este vehículo acaba de ser registrado por otra solicitud simultánea"),
    
    # --- Errores de Imágenes ---
    "error_existe_principal": (status.HTTP_400_BAD_REQUEST,"Este vehículo ya cuenta con una foto principal"),
    "foto_supera_tamano_maximo": (413, "La fotografía supera el tamaño máximo de 10 MB"),
    
    # --- Errores de cloudinary---
     "error_sub_nube": (status.HTTP_500_INTERNAL_SERVER_ERROR,"Error al subir la imagen en la nube"),
     "error_eliminar_de_nube": (status.HTTP_500_INTERNAL_SERVER_ERROR,"Error al eliminar la imagen de la nube"),
     
    # --- Errores de Usuarios ---
    "usuario_doc_existe": (status.HTTP_400_BAD_REQUEST,"El usuario con este número de documento ya existe"),
    "usuario_correo_existe": (status.HTTP_400_BAD_REQUEST,"El usuario con este correo electrónico ya existe"),
    "error_integridad_usuarios": (status.HTTP_409_CONFLICT,"Error de integridad: Se intentaron registrar usuarios de formasimultánea"),
    "usuario_doc_no_existe": (status.HTTP_404_NOT_FOUND,"El usuario con este número de documento no existe"),
    "usuario_id_no_existe": (status.HTTP_404_NOT_FOUND,"El usuario con este ID no existe"),
    
    # --- Control de Acceso y Roles ---
    "acceso_denegado": (status.HTTP_403_FORBIDDEN,"Acceso denegado: Esta operación requiere privilegios exclusivos de Administrador"),
    
    # --- Errores de Movimientos ---
    "no_hay_movimiento": (status.HTTP_404_NOT_FOUND,"Operación fallida: El vehículo asociado no se encuentra registrado o está inactivo"),
    "valor_nulo": (status.HTTP_400_BAD_REQUEST,"El valor de la operación debe ser mayor que cero"),
    "sin_resultados_filtrado": (status.HTTP_404_NOT_FOUND,"No se encontraron movimientos para los criterios seleccionados"),
    "sin_movimiento": (status.HTTP_404_NOT_FOUND,"Operación fallida. El movimiento no existe o se encuentra inactivo"),
    "error_eliminar": (status.HTTP_404_NOT_FOUND, "Operación fallida. No se pudo encontrar el movimiento a eliminar",
    ),
    
    #--- Errores de marcas y lineas ---
    "marca_duplicada": (status.HTTP_400_BAD_REQUEST,"La marca ya se encuentra registrada en el sistema"),
    "marca_no_existe": (status.HTTP_404_NOT_FOUND,"La marca especificada no existe"),
    "linea_duplicada": (status.HTTP_400_BAD_REQUEST,"Esta línea ya se encuentra registrada para la marca seleccionada"),
    "linea_no_existe": (status.HTTP_404_NOT_FOUND,"La línea especificada no existe"),
    
    #--- Error de fotografias
    "fotografia_no_existe": (status.HTTP_404_NOT_FOUND, "La fotografía especificada no existe.")
}


def error_http(clave: str) -> HTTPException:
  if clave in _ERRORES_CATALOGO:
    status_code, detail = _ERRORES_CATALOGO[clave]
    return HTTPException(status_code=status_code, detail=detail)
  return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor no especificado")
