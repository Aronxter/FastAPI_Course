from pydantic import BaseModel
from typing import Optional

#entidad usuario, tipado para validación de datos
class User(BaseModel):
    id: Optional[str]= None
    username: str
    email: str