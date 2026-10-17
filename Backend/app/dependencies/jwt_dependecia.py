from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.utils.security import SECRET_KEY, ALGORITHM
from app.schemas.token import DatosToken
from app.repositories.usuario_repository import UsurioRepository
from app.models.models_db import Usuario

esquema_oauth2 = OAuth2PasswordBearer(tokenUrl='/auth/token')

errores={
    "error_correo":HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El correo no esta registrado", headers={"WWW-Authenticate": "Bearer"}),
    "error_credenciales":HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Las credenciales no son validas", headers={"WWW-Authenticate": "Bearer"}),
    "error_token":HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El token de acceso no es valido", headers={"WWW-Authenticate": "Bearer"}),
    "usuario_inactivo":HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario se encuentra inactivo")
}

async def obtener_usuario_actual(token:Annotated[str, Depends(esquema_oauth2)], db:Session = Depends (get_db)) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo:str=payload.get("sub")
        if correo is None:
            raise errores["error_correo"]
        datos_token=DatosToken(correo=correo)
    except InvalidTokenError:
        raise errores["error_token"]
    usuario=UsurioRepository.get_por_correo(db=db,correo = datos_token.correo)
    if usuario is None:
        raise errores["error_credenciales"]
    return usuario

async def obtener_usuario_activo(usuario_actual:Annotated[Usuario, Depends(obtener_usuario_actual)]) -> Usuario:
    if not usuario_actual.activo:
        raise errores["usuario_inactivo"]
    return usuario_actual
