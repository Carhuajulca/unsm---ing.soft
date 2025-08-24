from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re


# ========================
# PRODUCT IMAGE SCHEMAS
# ========================

class ProductImageBase(BaseModel):
    url_image: str = Field(..., description="URL de la imagen del producto")
    alt_text: Optional[str] = Field(None, max_length=200, description="Texto alternativo para la imagen")
    sort_order: int = Field(0, ge=0, description="Orden de visualización de la imagen")
    is_primary: bool = Field(False, description="Indica si es la imagen principal")

    @field_validator('url_image')
    @classmethod
    def validate_image_url(cls, v: str) -> str:
        """Valida que la URL de imagen tenga un formato correcto"""
        if not re.match(r'^https?://.+\.(jpg|jpeg|png|gif|webp)$', v, re.IGNORECASE):
            raise ValueError('La URL debe ser válida y terminar en jpg, jpeg, png, gif o webp')
        return v


class ProductImageCreate(ProductImageBase):
    """Schema para crear una nueva imagen de producto"""
    product_id: int = Field(..., description="ID del producto al que pertenece la imagen")


class ProductImageUpdate(BaseModel):
    """Schema para actualizar una imagen de producto"""
    url_image: Optional[str] = None
    alt_text: Optional[str] = Field(None, max_length=200)
    sort_order: Optional[int] = Field(None, ge=0)
    is_primary: Optional[bool] = None

    @field_validator('url_image')
    @classmethod
    def validate_image_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^https?://.+\.(jpg|jpeg|png|gif|webp)$', v, re.IGNORECASE):
            raise ValueError('La URL debe ser válida y terminar en jpg, jpeg, png, gif o webp')
        return v


class ProductImageResponse(ProductImageBase):
    """Schema de respuesta para imagen de producto"""
    id: int
    product_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========================
# PRODUCT VARIANT SCHEMAS
# ========================

class ProductVariantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la variante (ej: Color, Talla)")
    value: str = Field(..., min_length=1, max_length=100, description="Valor de la variante (ej: Rojo, XL)")
    price_adjustment: Optional[Decimal] = Field(None, decimal_places=2, description="Ajuste de precio para esta variante")
    sku: str = Field(..., min_length=1, max_length=50, description="SKU único de la variante")

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v: str) -> str:
        """Valida que el SKU tenga el formato correcto"""
        if not re.match(r'^[A-Z0-9-_]+$', v):
            raise ValueError('El SKU solo puede contener letras mayúsculas, números, guiones y guiones bajos')
        return v.upper()

    @field_validator('price_adjustment')
    @classmethod
    def validate_price_adjustment(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Valida que el ajuste de precio no sea excesivamente negativo"""
        if v is not None and v < -9999.99:
            raise ValueError('El ajuste de precio no puede ser menor a -9999.99')
        return v


class ProductVariantCreate(ProductVariantBase):
    """Schema para crear una nueva variante de producto"""
    product_id: int = Field(..., description="ID del producto al que pertenece la variante")


class ProductVariantUpdate(BaseModel):
    """Schema para actualizar una variante de producto"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    value: Optional[str] = Field(None, min_length=1, max_length=100)
    price_adjustment: Optional[Decimal] = Field(None, decimal_places=2)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^[A-Z0-9-_]+$', v):
            raise ValueError('El SKU solo puede contener letras mayúsculas, números, guiones y guiones bajos')
        return v.upper()

    @field_validator('price_adjustment')
    @classmethod
    def validate_price_adjustment(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v < -9999.99:
            raise ValueError('El ajuste de precio no puede ser menor a -9999.99')
        return v


class ProductVariantResponse(ProductVariantBase):
    """Schema de respuesta para variante de producto"""
    id: int
    product_id: int
    created_at: datetime
    final_price: Optional[Decimal] = Field(None, description="Precio final calculado (precio base + ajuste)")
    
    model_config = ConfigDict(from_attributes=True)


# ========================
# PRODUCT SCHEMAS
# ========================

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del producto")
    slug: str = Field(..., min_length=1, max_length=200, description="Slug único para URLs")
    description: Optional[str] = Field(None, max_length=2000, description="Descripción del producto")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Precio del producto")
    compare_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2, description="Precio de comparación")
    sku: str = Field(..., min_length=1, max_length=50, description="SKU único del producto")
    category_id: int = Field(..., description="ID de la categoría del producto")

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Valida que el slug tenga el formato correcto"""
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('El slug solo puede contener letras minúsculas, números y guiones')
        if v.startswith('-') or v.endswith('-'):
            raise ValueError('El slug no puede empezar o terminar con guión')
        return v

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v: str) -> str:
        """Valida que el SKU tenga el formato correcto"""
        if not re.match(r'^[A-Z0-9-_]+$', v):
            raise ValueError('El SKU solo puede contener letras mayúsculas, números, guiones y guiones bajos')
        return v.upper()

    @field_validator('compare_price')
    @classmethod
    def validate_compare_price(cls, v: Optional[Decimal], info) -> Optional[Decimal]:
        """Valida que el precio de comparación sea mayor al precio base"""
        if v is not None and 'price' in info.data and v <= info.data['price']:
            raise ValueError('El precio de comparación debe ser mayor al precio base')
        return v


class ProductCreate(ProductBase):
    """Schema para crear un nuevo producto"""
    images: Optional[List[ProductImageBase]] = Field(default=[], description="Lista de imágenes del producto")
    variants: Optional[List[ProductVariantBase]] = Field(default=[], description="Lista de variantes del producto")

    @field_validator('images')
    @classmethod
    def validate_images(cls, v: List[ProductImageBase]) -> List[ProductImageBase]:
        """Valida que solo haya una imagen principal"""
        primary_count = sum(1 for img in v if img.is_primary)
        if primary_count > 1:
            raise ValueError('Solo puede haber una imagen principal')
        return v

    @field_validator('variants')
    @classmethod
    def validate_variants(cls, v: List[ProductVariantBase]) -> List[ProductVariantBase]:
        """Valida que no haya SKUs duplicados en las variantes"""
        skus = [variant.sku for variant in v]
        if len(skus) != len(set(skus)):
            raise ValueError('Los SKUs de las variantes deben ser únicos')
        return v


class ProductUpdate(BaseModel):
    """Schema para actualizar un producto"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    compare_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    category_id: Optional[int] = None

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('El slug solo puede contener letras minúsculas, números y guiones')
        if v.startswith('-') or v.endswith('-'):
            raise ValueError('El slug no puede empezar o terminar con guión')
        return v

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^[A-Z0-9-_]+$', v):
            raise ValueError('El SKU solo puede contener letras mayúsculas, números, guiones y guiones bajos')
        return v.upper()


# Schema simplificado para categoría (evita importaciones circulares)
class CategorySimple(BaseModel):
    """Schema simplificado de categoría para productos"""
    id: int
    name: str
    slug: str
    
    model_config = ConfigDict(from_attributes=True)


class ProductResponse(ProductBase):
    """Schema básico de respuesta para producto"""
    id: int
    category: Optional[CategorySimple] = None
    
    model_config = ConfigDict(from_attributes=True)


class ProductDetail(ProductResponse):
    """Schema detallado de producto con todas las relaciones"""
    images: List[ProductImageResponse] = []
    variants: List[ProductVariantResponse] = []
    primary_image: Optional[ProductImageResponse] = Field(None, description="Imagen principal del producto")
    discount_percentage: Optional[float] = Field(None, description="Porcentaje de descuento si hay precio de comparación")
    
    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """Schema para listado de productos"""
    id: int
    name: str
    slug: str
    price: Decimal
    compare_price: Optional[Decimal] = None
    sku: str
    category_id: int
    category_name: Optional[str] = None
    primary_image_url: Optional[str] = None
    variants_count: Optional[int] = None
    discount_percentage: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)


# Schema para filtros de búsqueda
class ProductFilters(BaseModel):
    """Schema para filtros de búsqueda de productos"""
    name: Optional[str] = Field(None, description="Buscar por nombre (contiene)")
    category_id: Optional[int] = Field(None, description="Filtrar por categoría")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Precio mínimo")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Precio máximo")
    sku: Optional[str] = Field(None, description="Buscar por SKU")
    has_discount: Optional[bool] = Field(None, description="Solo productos con descuento")
    in_stock: Optional[bool] = Field(None, description="Solo productos en stock")

    @field_validator('max_price')
    @classmethod
    def validate_price_range(cls, v: Optional[Decimal], info) -> Optional[Decimal]:
        """Valida que el precio máximo sea mayor al mínimo"""
        if v is not None and 'min_price' in info.data and info.data['min_price'] and v <= info.data['min_price']:
            raise ValueError('El precio máximo debe ser mayor al precio mínimo')
        return v


# Schema para respuesta paginada
class ProductPaginatedResponse(BaseModel):
    """Schema para respuesta paginada de productos"""
    items: List[ProductList]
    total: int
    page: int = Field(ge=1)
    size: int = Field(ge=1, le=100)
    pages: int
    has_next: bool
    has_prev: bool
    
    model_config = ConfigDict(from_attributes=True)


# Schema para operaciones bulk
class ProductBulkUpdate(BaseModel):
    """Schema para actualización masiva de productos"""
    product_ids: List[int] = Field(..., min_length=1, description="Lista de IDs de productos a actualizar")
    category_id: Optional[int] = None
    price_adjustment: Optional[Decimal] = Field(None, description="Ajuste de precio a aplicar")
    price_adjustment_type: Optional[str] = Field("fixed", regex="^(fixed|percentage)$", description="Tipo de ajuste: fixed o percentage")

    @field_validator('price_adjustment_type')
    @classmethod
    def validate_price_adjustment_type(cls, v: str, info) -> str:
        """Valida que si hay ajuste de precio, también esté el tipo"""
        if 'price_adjustment' in info.data and info.data['price_adjustment'] is not None and v is None:
            raise ValueError('Debe especificar el tipo de ajuste de precio')
        return v


# Schema para respuesta de operaciones bulk
class ProductBulkResponse(BaseModel):
    """Schema para respuestas de operaciones masivas"""
    success: bool
    message: str
    affected_products: List[int] = []
    errors: List[str] = []