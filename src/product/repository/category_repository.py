from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from src.product.models.category_model import Category
from src.core.base_repository import BaseRepository



class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        stmt = select(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        stmt = select(Category).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()  # Para obtener el id generado antes del commit
        return category

    async def update(self, category_id: int, data: dict) -> Optional[Category]:
        stmt = (
            update(Category)
            .where(Category.id == category_id)
            .values(**data)
            .returning(Category)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete(self, category_id: int) -> None:
        stmt = delete(Category).where(Category.id == category_id)
        await self.session.execute(stmt)

    # Ejemplo: obtener categorías padre
    async def get_parent_categories(self) -> List[Category]:
        stmt = select(Category).where(Category.parent_id == None)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Ejemplo: obtener subcategorías de una categoría
    async def get_subcategories(self, parent_id: int) -> List[Category]:
        stmt = select(Category).where(Category.parent_id == parent_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
