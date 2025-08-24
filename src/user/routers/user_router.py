from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.user.repository.user_repository import UserRepository
from src.user.services.user_service import UserService
from src.user.schemas.user_schema import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from src.user.models.user_model import User
from src.core.auth import get_current_user, get_current_active_user
from typing import List, Optional

router = APIRouter()

# Dependency para obtener el servicio
async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)

@router.post("/register", response_model=UserResponseSchema)
async def register_user(
    user: UserCreateSchema, 
    service: UserService = Depends(get_user_service)
):
    """
    Registrar un nuevo usuario (público).
    """
    return await service.register_user(user)

@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener usuario por ID (requiere autenticación).
    """
    # Solo permitir ver el propio perfil o si es admin (aquí puedes agregar lógica de roles)
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este usuario"
        )
    
    return await user_service.get_user_by_id(user_id)

@router.get("/", response_model=List[UserResponseSchema])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de usuarios (requiere autenticación).
    """
    return await user_service.get_users(skip, limit, is_active)

@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(
    user_id: int,
    user_data: UserUpdateSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar usuario (requiere autenticación).
    """
    # Solo permitir actualizar el propio perfil
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este usuario"
        )
    
    return await user_service.update_user(user_id, user_data)

@router.patch("/{user_id}/toggle-status", response_model=UserResponseSchema)
async def toggle_user_status(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Cambiar estado activo/inactivo (requiere autenticación).
    """
    # Solo permitir cambiar el propio estado
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para cambiar el estado de este usuario"
        )
    
    return await user_service.toggle_user_status(user_id)

@router.delete("/{user_id}/soft", response_model=UserResponseSchema)
async def soft_delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """
    Soft delete - marcar como inactivo (requiere autenticación).
    """
    # Solo permitir desactivar la propia cuenta
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para desactivar este usuario"
        )
    
    return await user_service.soft_delete_user(user_id)

@router.delete("/{user_id}/hard")
async def hard_delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Hard delete - eliminar físicamente (requiere autenticación).
    """
    # Solo permitir eliminar la propia cuenta
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este usuario"
        )
    
    success = await user_service.hard_delete_user(user_id)
    return {"message": "Usuario eliminado exitosamente" if success else "Error al eliminar"}

@router.get("/count/total")
async def count_users(
    is_active: Optional[bool] = None,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Contar total de usuarios (requiere autenticación).
    """
    count = await user_service.count_users(is_active)
    return {"total": count}

@router.get("/profile/me", response_model=UserResponseSchema)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Obtener el perfil del usuario actual.
    """
    return current_user

    