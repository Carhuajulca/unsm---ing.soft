from fastapi import HTTPException, status
from typing import List, Optional
from src.product.repository.category_repository import CategoryRepository
from src.product.schemas.category_schema import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)



class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository  

    async def get_all_categories(self) -> List[CategoryResponseSchema]:
        categories = await self.repository.get_all()
        return categories

    async def get_category_by_id(self, category_id: int) -> CategoryResponseSchema:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        return category

    async def create_category(self, category_data: CategoryCreateSchema) -> CategoryResponseSchema:
        # validación extra si quieres evitar duplicados
        existing = await self.repository.get_by_slug(category_data.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this slug already exists"
            )

        new_category = await self.repository.create(category_data)
        return new_category

    async def update_category(self, category_id: int, category_data: CategoryUpdateSchema) -> CategoryResponseSchema:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )

        updated_category = await self.repository.update(category_id, category_data)
        return updated_category

    async def delete_category(self, category_id: int) -> dict:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )

        await self.repository.delete(category_id)
        return {"message": "Category deleted successfully"}
