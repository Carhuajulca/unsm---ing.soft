from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    email: EmailStr = Field(..., max_length=100, description="Correo electrónico único")
    is_active: bool = Field(default=True, description="Estado del usuario activo/inactivo")

    


class UserCreate(UserBase):
    @field_validator('username')
    @classmethod
    def validate_name(cls, v: str) -> str:
        # Eliminar espacios extra y capitalizar
        v = ' '.join(v.split())  # Elimina espacios múltiples
        if not v.replace(' ', '').isalpha():
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.title()
    
    @field_validator('email')
    @classmethod
    def validate_email_lowercase(cls, v: str) -> str:
        return v.lower()  # Convertir email a minúsculas