from app.schemas.base import *

class TokenResponse(ConConfigBaseModel):
  access_token: str
  token_type: str


class DatosToken(ConConfigBaseModel):
  correo: Optional[str] = None