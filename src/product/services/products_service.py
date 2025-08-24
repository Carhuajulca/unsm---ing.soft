from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_, desc, asc
from sqlalchemy.orm import selectinload, joinedload
from src.models.product_models import Category, Product, ProductImage, ProductVariant
from .base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repositorio para operaciones básicas de acceso a datos de categorías"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, category_data: dict) -> Category:
        """Crear categoría en la base de datos"""
        db_category = Category(**category_data)
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        """Obtener categoría por ID"""
        result = await self.db.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        """Obtiene una categoría por su slug"""
        result = await self.db.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Obtener todas las categorías con paginación"""
        query = select(Category).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_active_status(self, is_active: bool, skip: int = 0, limit: int = 100) -> List[Category]:
        """Obtiene categorías por estado activo"""
        query = (
            select(Category)
            .where(Category.is_active == is_active)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_parent_id(self, parent_id: Optional[int]) -> List[Category]:
        """Obtiene categorías por ID padre"""
        if parent_id is None:
            query = select(Category).where(Category.parent_id.is_(None))
        else:
            query = select(Category).where(Category.parent_id == parent_id)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_with_children(self, category_id: int) -> Optional[Category]:
        """Obtiene una categoría con sus hijos cargados"""
        query = (
            select(Category)
            .options(selectinload(Category.children))
            .where(Category.id == category_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name_like(self, name_pattern: str) -> List[Category]:
        """Obtiene categorías que coincidan con un patrón de nombre"""
        query = select(Category).where(Category.name.ilike(f"%{name_pattern}%"))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_description_like(self, description_pattern: str) -> List[Category]:
        """Obtiene categorías que coincidan con un patrón de descripción"""
        query = select(Category).where(Category.description.ilike(f"%{description_pattern}%"))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_ordered_by_sort(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Obtiene categorías ordenadas por sort_order"""
        query = (
            select(Category)
            .order_by(Category.sort_order, Category.name)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, category_id: int, update_data: dict) -> Optional[Category]:
        """Actualizar categoría por ID"""
        await self.db.execute(
            update(Category)
            .where(Category.id == category_id)
            .values(**update_data)
        )
        await self.db.commit()
        return await self.get_by_id(category_id)

    async def delete(self, category_id: int) -> bool:
        """Eliminar categoría físicamente"""
        result = await self.db.execute(
            delete(Category).where(Category.id == category_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """Contar total de categorías"""
        query = select(func.count(Category.id))
        result = await self.db.execute(query)
        return result.scalar()

    async def count_by_active_status(self, is_active: bool) -> int:
        """Contar categorías por estado activo"""
        query = select(func.count(Category.id)).where(Category.is_active == is_active)
        result = await self.db.execute(query)
        return result.scalar()

    async def exists_by_slug_excluding_id(self, slug: str, category_id: int) -> bool:
        """Verificar si existe un slug excluyendo un ID específico"""
        result = await self.db.execute(
            select(Category).where(Category.slug == slug, Category.id != category_id)
        )
        return result.scalar_one_or_none() is not None


class ProductRepository(BaseRepository[Product]):
    """Repositorio para operaciones básicas de acceso a datos de productos"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, product_data: dict) -> Product:
        """Crear producto en la base de datos"""
        db_product = Product(**product_data)
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Obtener producto por ID"""
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Product]:
        """Obtiene un producto por su slug"""
        result = await self.db.execute(select(Product).where(Product.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """Obtiene un producto por su SKU"""
        result = await self.db.execute(select(Product).where(Product.sku == sku))
        return result.scalar_one_or_none()

    async def get_with_category(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto con su categoría cargada"""
        query = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id == product_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_with_images(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto con sus imágenes cargadas"""
        query = (
            select(Product)
            .options(selectinload(Product.images))
            .where(Product.id == product_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_with_variants(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto con sus variantes cargadas"""
        query = (
            select(Product)
            .options(selectinload(Product.variants))
            .where(Product.id == product_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_with_all_relations(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto con todas sus relaciones cargadas"""
        query = (
            select(Product)
            .options(
                joinedload(Product.category),
                selectinload(Product.images),
                selectinload(Product.variants)
            )
            .where(Product.id == product_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtener todos los productos con paginación"""
        query = select(Product).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_category_id(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene productos por ID de categoría"""
        query = (
            select(Product)
            .where(Product.category_id == category_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_name_like(self, name_pattern: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene productos que coincidan con un patrón de nombre"""
        query = (
            select(Product)
            .where(Product.name.ilike(f"%{name_pattern}%"))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_description_like(self, description_pattern: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene productos que coincidan con un patrón de descripción"""
        query = (
            select(Product)
            .where(Product.description.ilike(f"%{description_pattern}%"))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_price_range(self, min_price: float, max_price: float, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene productos por rango de precios"""
        query = (
            select(Product)
            .where(
                and_(
                    Product.price >= min_price,
                    Product.price <= max_price
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_ordered_by_price(self, ascending: bool = True, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene productos ordenados por precio"""
        order_func = asc if ascending else desc
        query = (
            select(Product)
            .order_by(order_func(Product.price))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count(self) -> int:
        """Contar total de productos"""
        query = select(func.count(Product.id))
        result = await self.db.execute(query)
        return result.scalar()

    async def count_by_category_id(self, category_id: int) -> int:
        """Cuenta productos por ID de categoría"""
        query = select(func.count(Product.id)).where(Product.category_id == category_id)
        result = await self.db.execute(query)
        return result.scalar()

    async def update(self, product_id: int, update_data: dict) -> Optional[Product]:
        """Actualizar producto por ID"""
        await self.db.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(**update_data)
        )
        await self.db.commit()
        return await self.get_by_id(product_id)

    async def delete(self, product_id: int) -> bool:
        """Eliminar producto físicamente"""
        result = await self.db.execute(
            delete(Product).where(Product.id == product_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def exists_by_slug_excluding_id(self, slug: str, product_id: int) -> bool:
        """Verificar si existe un slug excluyendo un ID específico"""
        result = await self.db.execute(
            select(Product).where(Product.slug == slug, Product.id != product_id)
        )
        return result.scalar_one_or_none() is not None

    async def exists_by_sku_excluding_id(self, sku: str, product_id: int) -> bool:
        """Verificar si existe un SKU excluyendo un ID específico"""
        result = await self.db.execute(
            select(Product).where(Product.sku == sku, Product.id != product_id)
        )
        return result.scalar_one_or_none() is not None


class ProductImageRepository(BaseRepository[ProductImage]):
    """Repositorio para operaciones básicas de acceso a datos de imágenes"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, image_data: dict) -> ProductImage:
        """Crear imagen de producto en la base de datos"""
        db_image = ProductImage(**image_data)
        self.db.add(db_image)
        await self.db.commit()
        await self.db.refresh(db_image)
        return db_image

    async def get_by_id(self, image_id: int) -> Optional[ProductImage]:
        """Obtener imagen por ID"""
        result = await self.db.execute(select(ProductImage).where(ProductImage.id == image_id))
        return result.scalar_one_or_none()

    async def get_by_product_id(self, product_id: int) -> List[ProductImage]:
        """Obtiene todas las imágenes de un producto"""
        query = select(ProductImage).where(ProductImage.product_id == product_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_product_id_ordered(self, product_id: int) -> List[ProductImage]:
        """Obtiene imágenes de un producto ordenadas por sort_order"""
        query = (
            select(ProductImage)
            .where(ProductImage.product_id == product_id)
            .order_by(ProductImage.sort_order, ProductImage.id)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_is_primary(self, product_id: int, is_primary: bool) -> List[ProductImage]:
        """Obtiene imágenes por estado de principal"""
        query = (
            select(ProductImage)
            .where(
                and_(
                    ProductImage.product_id == product_id,
                    ProductImage.is_primary == is_primary
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_first_by_is_primary(self, product_id: int, is_primary: bool) -> Optional[ProductImage]:
        """Obtiene la primera imagen por estado de principal"""
        query = (
            select(ProductImage)
            .where(
                and_(
                    ProductImage.product_id == product_id,
                    ProductImage.is_primary == is_primary
                )
            )
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_primary_status_by_product(self, product_id: int, is_primary: bool) -> bool:
        """Actualiza el estado de principal de todas las imágenes de un producto"""
        result = await self.db.execute(
            update(ProductImage)
            .where(ProductImage.product_id == product_id)
            .values(is_primary=is_primary)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def update_sort_order(self, image_id: int, sort_order: int) -> bool:
        """Actualiza el orden de una imagen específica"""
        result = await self.db.execute(
            update(ProductImage)
            .where(ProductImage.id == image_id)
            .values(sort_order=sort_order)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductImage]:
        """Obtener todas las imágenes con paginación"""
        query = select(ProductImage).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, image_id: int, update_data: dict) -> Optional[ProductImage]:
        """Actualizar imagen por ID"""
        await self.db.execute(
            update(ProductImage)
            .where(ProductImage.id == image_id)
            .values(**update_data)
        )
        await self.db.commit()
        return await self.get_by_id(image_id)

    async def delete(self, image_id: int) -> bool:
        """Eliminar imagen físicamente"""
        result = await self.db.execute(
            delete(ProductImage).where(ProductImage.id == image_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def delete_by_product_id(self, product_id: int) -> bool:
        """Elimina todas las imágenes de un producto"""
        result = await self.db.execute(
            delete(ProductImage).where(ProductImage.product_id == product_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """Contar total de imágenes"""
        query = select(func.count(ProductImage.id))
        result = await self.db.execute(query)
        return result.scalar()


class ProductVariantRepository(BaseRepository[ProductVariant]):
    """Repositorio para operaciones básicas de acceso a datos de variantes"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, variant_data: dict) -> ProductVariant:
        """Crear variante de producto en la base de datos"""
        db_variant = ProductVariant(**variant_data)
        self.db.add(db_variant)
        await self.db.commit()
        await self.db.refresh(db_variant)
        return db_variant

    async def get_by_id(self, variant_id: int) -> Optional[ProductVariant]:
        """Obtener variante por ID"""
        result = await self.db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
        return result.scalar_one_or_none()

    async def get_by_product_id(self, product_id: int) -> List[ProductVariant]:
        """Obtiene todas las variantes de un producto"""
        query = select(ProductVariant).where(ProductVariant.product_id == product_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_product_id_ordered(self, product_id: int) -> List[ProductVariant]:
        """Obtiene variantes de un producto ordenadas"""
        query = (
            select(ProductVariant)
            .where(ProductVariant.product_id == product_id)
            .order_by(ProductVariant.name, ProductVariant.value)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_sku(self, sku: str) -> Optional[ProductVariant]:
        """Obtiene una variante por su SKU"""
        result = await self.db.execute(select(ProductVariant).where(ProductVariant.sku == sku))
        return result.scalar_one_or_none()

    async def get_by_name_and_product(self, product_id: int, variant_name: str) -> List[ProductVariant]:
        """Obtiene variantes de un producto por nombre específico"""
        query = (
            select(ProductVariant)
            .where(
                and_(
                    ProductVariant.product_id == product_id,
                    ProductVariant.name == variant_name
                )
            )
            .order_by(ProductVariant.value)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_value_and_product(self, product_id: int, variant_value: str) -> List[ProductVariant]:
        """Obtiene variantes de un producto por valor específico"""
        query = (
            select(ProductVariant)
            .where(
                and_(
                    ProductVariant.product_id == product_id,
                    ProductVariant.value == variant_value
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_name_and_value(self, product_id: int, name: str, value: str) -> Optional[ProductVariant]:
        """Obtiene una variante específica por nombre y valor"""
        query = (
            select(ProductVariant)
            .where(
                and_(
                    ProductVariant.product_id == product_id,
                    ProductVariant.name == name,
                    ProductVariant.value == value
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_distinct_names_by_product(self, product_id: int) -> List[str]:
        """Obtiene nombres únicos de variantes de un producto"""
        query = (
            select(ProductVariant.name)
            .where(ProductVariant.product_id == product_id)
            .distinct()
        )
        result = await self.db.execute(query)
        return [row for row in result.scalars().all()]

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductVariant]:
        """Obtener todas las variantes con paginación"""
        query = select(ProductVariant).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, variant_id: int, update_data: dict) -> Optional[ProductVariant]:
        """Actualizar variante por ID"""
        await self.db.execute(
            update(ProductVariant)
            .where(ProductVariant.id == variant_id)
            .values(**update_data)
        )
        await self.db.commit()
        return await self.get_by_id(variant_id)

    async def delete(self, variant_id: int) -> bool:
        """Eliminar variante físicamente"""
        result = await self.db.execute(
            delete(ProductVariant).where(ProductVariant.id == variant_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def delete_by_product_id(self, product_id: int) -> bool:
        """Elimina todas las variantes de un producto"""
        result = await self.db.execute(
            delete(ProductVariant).where(ProductVariant.product_id == product_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """Contar total de variantes"""
        query = select(func.count(ProductVariant.id))
        result = await self.db.execute(query)
        return result.scalar()

    async def exists_by_sku_excluding_id(self, sku: str, variant_id: int) -> bool:
        """Verificar si existe un SKU excluyendo un ID específico"""
        result = await self.db.execute(
            select(ProductVariant).where(ProductVariant.sku == sku, ProductVariant.id != variant_id)
        )
        return result.scalar_one_or_none() is not None