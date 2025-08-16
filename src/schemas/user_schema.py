from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional




# 1. Separar validaciones en una clase base
class UserValidations(BaseModel):
    """Solo las validaciones, sin campos"""
    
    @field_validator('first_name', 'last_name', mode='before', check_fields=False)
    @classmethod
    def validate_names(cls, v):
        if v is None:  # Para campos Optional
            return v
        v = ' '.join(str(v).split())
        if not v.replace(' ', '').isalpha():
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.title()

    @field_validator('email', mode='before', check_fields=False)
    @classmethod
    def validate_email_lowercase(cls, v):
        if v is None:  # Para campos Optional
            return v
        return str(v).lower()

# --- Base Schemas ---

class UserBase(UserValidations):
    user : str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    first_name: str = Field(..., min_length=3, max_length=50, description="Nombre")
    last_name: str = Field(..., min_length=3, max_length=100, description="Apellidos")
    email: EmailStr = Field(..., max_length=100, description="Correo electrónico único")
    is_active: bool = Field(default=True, description="Estado del usuario activo/inactivo")


# --- Create/Update Schemas ---

class UserCreateSchema(UserBase):
    pass

class UserUpdateSchema(UserValidations):
    first_name: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre de usuario")
    last_name: Optional[str] = Field(None, min_length=3, max_length=100, description="Apellidos del usuario")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico único")
    is_active: Optional[bool] = Field(None, description="Estado del usuario activo/inactivo")



# --- Response Schemas ---

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

class UserList(UserResponseSchema):
    pass

class UserDelete(BaseModel):
    id: int

# --- Custom/Alternative Response Schemas ---

class UserResponseWithAlias(BaseModel):
    id: int
    username: str = Field(alias="first_name")
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class UserResponseCustom(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def from_db_user(cls, user):
        return cls(
            id=user.id,
            username=user.first_name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

class UserResponseExact(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Action Response Schemas ---

class UserCreateResponse(UserResponseSchema):
    message: str = Field(default="Usuario creado exitosamente")

class UserUpdateResponse(UserResponseSchema):
    message: str = Field(default="Usuario actualizado exitosamente")

class UserDeleteResponse(BaseModel):
    id: int
    message: str = Field(default="Usuario eliminado exitosamente")
    deleted_at: datetime = Field(default_factory=datetime.now)
