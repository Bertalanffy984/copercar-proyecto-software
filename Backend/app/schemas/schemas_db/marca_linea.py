from app.schemas.base import *

class MarcaLineaTransaccionalCreate(ConConfigBaseModel):
    nombre_marca: str = Field(..., min_length=2, max_length=150)
    nombre_linea: str = Field(..., min_length=2, max_length=150)
    
    @field_validator("nombre_marca", "nombre_linea")
    @classmethod
    def limpiar_y_mayusculas(cls, v: str) -> str:
        return v.strip().upper()