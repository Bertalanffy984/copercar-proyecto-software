from fastapi import HTTPException,status

errores={
    "vehiculo_existe":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El vehiculo con esa placa ya existe (mirar en los carros inactivos si no se encuetra en los activos)"),
    "vehiculo_no_placa":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se encuentra un vehiculo con esa placa"),
    "error_id_vehiculo":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se encuentra un vehiculo con ese id"),
    "error_concurrencia_crear":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Conflicto de concurrencia: Este vehiculo acaba de ser registrado por otra solicitud simultanea"),
    #errores para imagenes
    "error_formato":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo proporcionado no es una imagen válida"),
    "error_existe_principal":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este vehiculo ya cuenta con una foto principal"),
    #errores para usuarios
    "usuario_doc_existe":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="EL usuario con este Numero de documento ya existe"),
    "usuario_correo_existe":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="EL usuario con este correo ya existe"),
    "error_integridad_usuarios":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error de integridad: (se intentaron agregar dos usuarios al mismo tiempo)"),
    "usuario_doc_no_existe":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="EL usuario con este Numero de documento no existe"),
    "usuario_id_no_existe":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="EL usuario con este id no existe"),
    #error por permisos de administrador
    "acceso_denegado":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Acceso denegado: Esta operación requiere privilegios exclusivos de Administrador"),
    #errores para movimientos
    "no_hay_movimiento":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operación fallida: El vehículo asociado no se encuentra registrado o esta inactivo."),
    "valor_nulo":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El valor de la operación debe ser mayor que cero."),
    "sin_resultados_filtrado":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se encontraron movimientos para los criterios seleccionados."),
    "sin_movimiento":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operación fallida. El movimiento no existe o se encuentra inactivo."),         
    "error_eliminar":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operación fallida. No se pudo encontrar el movimiento a eliminar"),         
}
