from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.schemas.token import TokenResponse
from app.schemas.BaseDB.usuario import UsuarioResponse
from app.services.auth_service import autenticar_usuario
from app.utils.security import ( crear_token_acceso, ACCESO_TOKEN_EXPIRACION_MINUTOS)
from app.dependencies.jwt_dependecia import obtener_usuario_activo
from app.models.models_db.Usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

errores={
    "error_credenciales" : HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos", headers={"WWW-Authenticate": "Bearer"})
}

@router.post("/token", response_model=TokenResponse, status_code=200)
async def iniciar_sesion(datos_formulario:Annotated[OAuth2PasswordRequestForm, Depends()], db: Session=Depends(get_db)):
    usuario=autenticar_usuario(db=db, correo=datos_formulario.username, contrasenia=datos_formulario.password)
    if not usuario:
        raise errores["error_credenciales"]
    
    expiracion_token=timedelta(minutes=ACCESO_TOKEN_EXPIRACION_MINUTOS)
    token_acceso=crear_token_acceso(datos={"sub":usuario.correo}, expiracion_delta = expiracion_token)
    return TokenResponse(access_token=token_acceso, token_type="bearer")

@router.get("/me", response_model=UsuarioResponse)
async def leer_usuario_actual(usuario_actual: Annotated[Usuario, Depends(obtener_usuario_activo)],):
  return usuario_actual