from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from src.core.security import create_access_token, verify_password
from src.core.config import settings
from src.database import get_db
from src.user.repository.user_repository import UserRepository
from src.user.models.user_model import User
from src.user.schemas.auth_schema import (
    Token, LoginResponse, LogoutResponse, UserInfo
)
from src.core.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

async def authenticate_user(email: str, password: str, db: AsyncSession) -> User:
    """
    Autentica un usuario con email y password usando la base de datos real.
    
    Args:
        email (str): Email del usuario
        password (str): Contraseña en texto plano
        db (AsyncSession): Sesión de base de datos
        
    Returns:
        User: Usuario autenticado o None si falla
    """
    user_repository = UserRepository(db)
    user = await user_repository.get_by_email(email)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    if not user.is_active:
        return None
    
    return user

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para iniciar sesión con email y contraseña.
    
    Args:
        form_data (OAuth2PasswordRequestForm): Formulario con username (email) y password
        db (AsyncSession): Sesión de base de datos
        
    Returns:
        LoginResponse: Token de acceso y información del usuario
        
    Raises:
        HTTPException: Si las credenciales son incorrectas
    """
    # Usar email como username
    user = await authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    # Actualizar último login
    user_repository = UserRepository(db)
    await user_repository.update(user.id, {"last_login_at": timedelta()})
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active
        },
        message="Login exitoso"
    )

@router.post("/login-json", response_model=LoginResponse)
async def login_json(
    login_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint alternativo para login usando JSON.
    
    Args:
        login_data (dict): {"email": "...", "password": "..."}
        db (AsyncSession): Sesión de base de datos
        
    Returns:
        LoginResponse: Token de acceso y información del usuario
    """
    email = login_data.get("email")
    password = login_data.get("password")
    
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email y contraseña son requeridos"
        )
    
    user = await authenticate_user(email, password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active
        },
        message="Login exitoso"
    )

@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Endpoint para cerrar sesión (logout).
    
    Args:
        current_user (User): Usuario actual autenticado
        
    Returns:
        LogoutResponse: Confirmación de logout
    """
    # En una implementación más avanzada, aquí podrías:
    # - Agregar el token a una lista negra
    # - Invalidar refresh tokens
    # - Registrar el logout en la base de datos
    
    return LogoutResponse(
        message=f"Logout exitoso para {current_user.email}",
        timestamp=timedelta()
    )

@router.get("/me", response_model=UserInfo)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Obtiene información del usuario actual.
    
    Args:
        current_user (User): Usuario actual autenticado
        
    Returns:
        UserInfo: Información del usuario
    """
    return UserInfo(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    """
    Verifica si el token es válido.
    
    Args:
        current_user (User): Usuario actual autenticado
        
    Returns:
        dict: Confirmación de token válido
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "email": current_user.email,
        "message": "Token válido"
    }
