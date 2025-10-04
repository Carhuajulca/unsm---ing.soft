
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from src.product.models.product_model import Product
from src.core.base_repository import BaseRepository



class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        stmt = select(Product).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()  # genera el id sin commit
        return product

    async def update(self, product_id: int, data: dict) -> Optional[Product]:
        stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(**data)
            .returning(Product)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete(self, product_id: int) -> None:
        stmt = delete(Product).where(Product.id == product_id)
        await self.session.execute(stmt)

    # Ejemplo: obtener productos por categoría
    async def get_by_category(self, category_id: int) -> List[Product]:
        stmt = select(Product).where(Product.category_id == category_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Ejemplo: obtener productos con sus variantes
    async def get_with_variants(self, product_id: int) -> Optional[Product]:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                # Cargar variantes e imágenes si usas relationship en el modelo
                # joinedload(Product.variants),
                # joinedload(Product.images),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
