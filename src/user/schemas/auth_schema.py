"""
Esquemas para autenticación JWT
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    """Esquema para respuesta de token"""
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")
    user: dict = Field(..., description="Información del usuario")

class TokenData(BaseModel):
    """Esquema para datos del token"""
    user_id: Optional[int] = None
    email: Optional[str] = None

class LoginRequest(BaseModel):
    """Esquema para solicitud de login"""
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")

class LoginResponse(BaseModel):
    """Esquema para respuesta de login"""
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")
    user: dict = Field(..., description="Información del usuario")
    message: str = Field(default="Login exitoso", description="Mensaje de respuesta")

class LogoutResponse(BaseModel):
    """Esquema para respuesta de logout"""
    message: str = Field(default="Logout exitoso", description="Mensaje de confirmación")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del logout")

class RefreshTokenRequest(BaseModel):
    """Esquema para solicitud de refresh token"""
    refresh_token: str = Field(..., description="Refresh token")

class RefreshTokenResponse(BaseModel):
    """Esquema para respuesta de refresh token"""
    access_token: str = Field(..., description="Nuevo token de acceso JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")

class UserInfo(BaseModel):
    """Esquema para información básica del usuario"""
    id: int = Field(..., description="ID del usuario")
    email: str = Field(..., description="Email del usuario")
    first_name: str = Field(..., description="Nombre del usuario")
    last_name: str = Field(..., description="Apellido del usuario")
    is_active: bool = Field(..., description="Estado del usuario")
    created_at: datetime = Field(..., description="Fecha de creación")

    class Config:
        from_attributes = True
