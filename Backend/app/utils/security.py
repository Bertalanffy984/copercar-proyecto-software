from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
import jwt, os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESO_TOKEN_EXPIRACION_MINUTOS = int(os.getenv("ACCESO_TOKEN_EXPIRACION_MINUTOS"))
administrador_hash = PasswordHash.recommended()

def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
  return administrador_hash.verify(contrasena_plana, contrasena_hash)

def obtener_hash_contrasena(contrasena: str) -> str:
  return administrador_hash.hash(contrasena)

def crear_token_acceso(datos: dict, expiracion_delta: timedelta | None = None) -> str:
    datos_codificados=datos.copy()
    if expiracion_delta:
        expiracion=datetime.now(timezone.utc) + expiracion_delta
    else:
        expiracion=datetime.now(timezone.utc) + timedelta(minutes=ACCESO_TOKEN_EXPIRACION_MINUTOS)
    datos_codificados.update({"exp" : expiracion})
    token_jwt = jwt.encode(datos_codificados, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt