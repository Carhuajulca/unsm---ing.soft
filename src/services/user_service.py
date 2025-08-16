from fastapi import HTTPException, status
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from src.models.users import User
from typing import List, Optional

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreateSchema) -> User:
        """Crear un nuevo usuario con validaciones de negocio"""
        # Validación: email único
        existing_email = await self.user_repository.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )

        # Validación: username único
        existing_username = await self.user_repository.get_by_username(user_data.first_name)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso"
            )

        # Preparar datos para el repository
        user_dict = {
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "is_active": user_data.is_active
        }

        return await self.user_repository.create(user_dict)
# --------------------------------------------------------------------------------------   

    async def get_user_by_id(self, user_id: int) -> User:
        """Obtener usuario por ID con validación de existencia"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return await self.user_repository.get_by_email(email)

    async def get_user_by_username(self, first_name: str) -> Optional[User]:
        """Obtener usuario por username"""
        return await self.user_repository.get_by_username(first_name)

    async def get_users(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        is_active: Optional[bool] = None
    ) -> List[User]:
        """Obtener lista de usuarios con paginación"""
        # Validación de parámetros
        if limit > 100:
            limit = 100
        if skip < 0:
            skip = 0

        return await self.user_repository.get_all(skip, limit, is_active)

    async def count_users(self, is_active: Optional[bool] = None) -> int:
        """Contar total de usuarios"""
        return await self.user_repository.count(is_active)

    async def update_user(self, user_id: int, user_data: UserUpdateSchema) -> User:
        """Actualizar usuario con validaciones de negocio"""
        # Verificar que el usuario existe
        existing_user = await self.get_user_by_id(user_id)

        # Preparar datos para actualizar
        update_data = {}

        # Validar y preparar username
        if user_data.name is not None:
            if await self.user_repository.exists_by_username_excluding_id(
                user_data.name, user_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya está en uso"
                )
            update_data['name'] = user_data.name

        # Validar y preparar email
        if user_data.email is not None:
            if await self.user_repository.exists_by_email_excluding_id(
                user_data.email, user_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
            update_data['email'] = user_data.email

        # Preparar is_active
        if user_data.is_active is not None:
            update_data['is_active'] = user_data.is_active

        # Si no hay datos para actualizar, retornar usuario actual
        if not update_data:
            return existing_user

        # Actualizar en repository
        updated_user = await self.user_repository.update(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar usuario"
            )

        return updated_user

    async def toggle_user_status(self, user_id: int) -> User:
        """Cambiar estado activo/inactivo del usuario"""
        user = await self.get_user_by_id(user_id)
        
        update_data = {"is_active": not user.is_active}
        updated_user = await self.user_repository.update(user_id, update_data)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al cambiar estado del usuario"
            )

        return updated_user

    async def soft_delete_user(self, user_id: int) -> User:
        """Eliminar usuario (soft delete - marcar como inactivo)"""
        user = await self.get_user_by_id(user_id)
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya está inactivo"
            )

        update_data = {"is_active": False}
        updated_user = await self.user_repository.update(user_id, update_data)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al desactivar usuario"
            )

        return updated_user

    async def hard_delete_user(self, user_id: int) -> bool:
        """Eliminar usuario físicamente de la base de datos"""
        # Verificar que el usuario existe
        await self.get_user_by_id(user_id)
        
        # Aquí podrías agregar lógica de negocio adicional
        # como verificar si el usuario tiene dependencias
        
        return await self.user_repository.delete(user_id)

