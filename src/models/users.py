from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from src.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=True)  # Para login tradicional
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # # Campos para OAuth2
    # provider = Column(String, nullable=True)  # 'google', 'facebook', 'github', etc.
    # provider_id = Column(String, nullable=True)  # ID del usuario en el proveedor
    # access_token = Column(Text, nullable=True)  # Token de acceso (puede ser largo)
    # refresh_token = Column(Text, nullable=True)  # Token para renovar el access_token
    # token_expires_at = Column(DateTime(timezone=True), nullable=True)  # Cuándo expira el token
    # scope = Column(String, nullable=True)  # Permisos otorgados
    
    # # Campos adicionales útiles
    # avatar_url = Column(String, nullable=True)  # URL del avatar del usuario
    # locale = Column(String, nullable=True)  # Idioma/región del usuario
    
    # # Para autenticación tradicional (opcional si solo usas OAuth2)
    # is_verified = Column(Boolean, default=False)  # Si el email está verificado