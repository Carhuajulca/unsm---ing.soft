from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.schemas.users.user import UserCreate, UserUpdate, UserResponse
from typing import List, Optional

router = APIRouter()

# Dependency para obtener el servicio
async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Crear un nuevo usuario"""
    return await user_service.create_user(user_data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Obtener usuario por ID"""
    return await user_service.get_user_by_id(user_id)

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    user_service: UserService = Depends(get_user_service)
):
    """Obtener lista de usuarios"""
    return await user_service.get_users(skip, limit, is_active)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Actualizar usuario"""
    return await user_service.update_user(user_id, user_data)

@router.patch("/{user_id}/toggle-status", response_model=UserResponse)
async def toggle_user_status(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Cambiar estado activo/inactivo"""
    return await user_service.toggle_user_status(user_id)

@router.delete("/{user_id}/soft", response_model=UserResponse)
async def soft_delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Soft delete - marcar como inactivo"""
    return await user_service.soft_delete_user(user_id)

@router.delete("/{user_id}/hard")
async def hard_delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Hard delete - eliminar físicamente"""
    success = await user_service.hard_delete_user(user_id)
    return {"message": "Usuario eliminado exitosamente" if success else "Error al eliminar"}

@router.get("/count/total")
async def count_users(
    is_active: Optional[bool] = None,
    user_service: UserService = Depends(get_user_service)
):
    """Contar total de usuarios"""
    count = await user_service.count_users(is_active)
    return {"total": count}

    