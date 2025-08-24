from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from typing import List, Optional
from src.product.schemas.product_schema import *
from src.product.repository.product_repository import ProductRepository
from src.product.services.product_service import ProductService

router = APIRouter()

@router.post("/products/", response_model=ProductResponseSchema)
async def create_product(
    product: ProductCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(ProductRepository(db))
    return await service.create_product(product)

@router.get("/products/", response_model=List[ProductResponseSchema])
async def list_products(
    skip: int = 0,
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(ProductRepository(db))
    return await service.list_products(skip=skip, limit=limit)

@router.get("/products/{product_id}", response_model=ProductResponseSchema)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(ProductRepository(db))
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=ProductResponseSchema)
async def update_product(
    product_id: int,
    product: ProductUpdateSchema,
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(ProductRepository(db))
    updated_product = await service.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}", response_model=dict)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(ProductRepository(db))
    deleted = await service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
