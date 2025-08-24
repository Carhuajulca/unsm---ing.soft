from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

# --- Validaciones reutilizables ---
class UserValidations(BaseModel):
    """Validaciones reutilizables"""
    
    @field_validator('first_name', 'last_name', mode='before', check_fields=False)
    @classmethod
    def validate_names(cls, v):
        if v is None:
            return v
        v = ' '.join(str(v).split())
        if not v.replace(' ', '').isalpha():
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.title()

    @field_validator('email', mode='before', check_fields=False)
    @classmethod
    def validate_email_lowercase(cls, v):
        if v is None:
            return v
        return str(v).lower()

# --- Base Schema ---
class UserBase(UserValidations):
    first_name: str = Field(..., min_length=3, max_length=50, description="Nombre")
    last_name: str = Field(..., min_length=3, max_length=100, description="Apellidos")
    email: EmailStr = Field(..., max_length=100, description="Correo electrónico único")
    is_active: bool = Field(default=True, description="Estado del usuario activo/inactivo")

# --- Create / Update ---
class UserCreateSchema(UserBase):
    password: str = Field(..., min_length=6, max_length=128, description="Contraseña del usuario")

class UserUpdateSchema(UserValidations):
    first_name: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre de usuario")
    last_name: Optional[str] = Field(None, min_length=3, max_length=100, description="Apellidos del usuario")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico único")
    is_active: Optional[bool] = Field(None, description="Estado del usuario activo/inactivo")
    password: Optional[str] = Field(None, min_length=6, max_length=128, description="Nueva contraseña")

# --- Response ---
class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserCreateResponse(UserResponseSchema):
    message: str = Field(default="Usuario creado exitosamente")

class UserUpdateResponse(UserResponseSchema):
    message: str = Field(default="Usuario actualizado exitosamente")

class UserDeleteResponse(BaseModel):
    id: int
    message: str = Field(default="Usuario eliminado exitosamente")
    deleted_at: datetime = Field(default_factory=datetime.now)
