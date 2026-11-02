from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic import Field, field_validator
class ConConfigBaseModel(BaseModel):
  model_config = ConfigDict(from_attributes=True)

__all__ = [
    "date",
    "datetime",
    "Decimal",
    "List",
    "Optional",
    "BaseModel",
    "ConfigDict",
    "EmailStr",
    "Field",
    "field_validator",
    "ConConfigBaseModel",
]