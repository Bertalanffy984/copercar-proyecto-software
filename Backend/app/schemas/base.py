from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

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
    "ConConfigBaseModel",
]