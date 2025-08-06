from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from src.models.model import User
from typing import List, Optional
from ..base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, user_data: dict) -> User:
        """Crear usuario en la base de datos"""
        db_user = User(**user_data)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        result = await self.db.execute(select(User).where(User.name == username))
        return result.scalar_one_or_none()

    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        is_active: Optional[bool] = None) -> List[User]:
        """Obtener todos los usuarios con filtros y paginación"""
        query = select(User)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count(self, is_active: Optional[bool] = None) -> int:
        """Contar total de usuarios"""
        query = select(func.count(User.id))
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        result = await self.db.execute(query)
        return result.scalar()

    async def update(self, user_id: int, update_data: dict) -> Optional[User]:
        """Actualizar usuario por ID"""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
        )
        await self.db.commit()
        
        # Obtener el usuario actualizado
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        """Eliminar usuario físicamente"""
        result = await self.db.execute(
            delete(User).where(User.id == user_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def exists_by_email_excluding_id(self, email: str, user_id: int) -> bool:
        """Verificar si existe un email excluyendo un ID específico"""
        result = await self.db.execute(
            select(User).where(User.email == email, User.id != user_id)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_username_excluding_id(self, username: str, user_id: int) -> bool:
        """Verificar si existe un username excluyendo un ID específico"""
        result = await self.db.execute(
            select(User).where(User.name == username, User.id != user_id)
        )
        return result.scalar_one_or_none() is not None
