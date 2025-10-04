from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.product.repository.category_repository import CategoryRepository
from src.product.services.category_service import CategoryService
from src.product.schemas.category_schema import CategoryResponseSchema, CategoryCreateSchema, CategoryUpdateSchema
from typing import List, Optional
from src.product.services.category_service import CategoryService


router = APIRouter()

@router.post("/categories/", response_model=CategoryResponseSchema)
async def create_category(
    category: CategoryCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    service = CategoryService(CategoryRepository(db))
    return await service.create_category(category)

@router.get("/categories/", response_model=List[CategoryResponseSchema])
async def list_categories(
    skip: int = 0,
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    service = CategoryService(CategoryRepository(db))
    return await service.list_categories(skip=skip, limit=limit)

@router.get("/categories/{category_id}", response_model=CategoryResponseSchema)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = CategoryService(CategoryRepository(db))
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=CategoryResponseSchema)
async def update_category(
    category_id: int,
    category: CategoryUpdateSchema,
    db: AsyncSession = Depends(get_db)
):
    service = CategoryService(CategoryRepository(db))
    updated_category = await service.update_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/categories/{category_id}", response_model=dict)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = CategoryService(CategoryRepository(db))
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted"}