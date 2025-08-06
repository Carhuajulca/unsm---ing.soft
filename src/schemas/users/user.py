from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    email: EmailStr = Field(..., max_length=100, description="Correo electrónico único")
    is_active: bool = Field(default=True, description="Estado del usuario activo/inactivo")

class UserCreate(UserBase):
    @field_validator('name')
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

# SOLUCIÓN 1: Modelo que coincide con tu SQLAlchemy (más probable)
class UserResponse(BaseModel):
    """Modelo de respuesta - campos que coinciden con tu modelo SQLAlchemy"""
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# SOLUCIÓN 2: Si quieres mantener 'username' en la respuesta pero tu BD tiene 'name'
class UserResponseWithMapping(BaseModel):
    """Modelo de respuesta con mapeo de campos"""
    id: int
    username: str = Field(alias="name")  # Mapea 'name' de BD a 'username' en respuesta
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True

# SOLUCIÓN 3: Método personalizado para casos complejos
class UserResponseCustom(BaseModel):
    """Modelo con método personalizado de mapeo"""
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def from_db_user(cls, user):
        """Crea una instancia desde el modelo SQLAlchemy"""
        return cls(
            id=user.id,
            username=user.name,  # Mapeo manual de 'name' a 'username'
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

class UserList(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (antes orm_mode = True)

class UserDelete(BaseModel):
    id: int

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre de usuario")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico único")
    is_active: Optional[bool] = Field(None, description="Estado del usuario activo/inactivo")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v is None:
            return v
        v = ' '.join(v.split())
        if not v.replace(' ', '').isalpha():
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.title()

    @field_validator('email')
    @classmethod
    def validate_email_lowercase(cls, v: str) -> str:
        if v is None:
            return v
        return v.lower()

# Alternativa: Usar alias para mapear campos con nombres diferentes
class UserResponseWithAlias(BaseModel):
    """Modelo de respuesta usando alias para mapear campos"""
    id: int
    username: str = Field(alias="name")  # Si en BD se llama 'name'
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True  # Permite usar tanto el nombre original como el alias

# O crear un modelo que coincida exactamente con tu modelo de BD
class UserResponseExact(BaseModel):
    """Modelo que coincide exactamente con los campos de tu modelo SQLAlchemy"""
    id: int
    name: str  # Cambiar a 'name' si así se llama en tu BD
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
class UserCreateResponse(UserResponse):
    """Respuesta específica para creación de usuario"""
    message: str = Field(default="Usuario creado exitosamente")

class UserUpdateResponse(UserResponse):
    """Respuesta específica para actualización de usuario"""
    message: str = Field(default="Usuario actualizado exitosamente")

class UserDeleteResponse(BaseModel):
    """Respuesta para eliminación de usuario"""
    id: int
    message: str = Field(default="Usuario eliminado exitosamente")
    deleted_at: datetime = Field(default_factory=datetime.now)