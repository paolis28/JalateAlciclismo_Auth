from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    correo: EmailStr
    contrasena: str
    url_foto: Optional[str] = None
