from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re


# Schema base con campos comunes
class CategoryBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la categoría")
    slug: str = Field(..., min_length=1, max_length=100, description="Slug único para URLs")
    description: Optional[str] = Field(None, max_length=500, description="Descripción de la categoría")
    image_url: Optional[str] = Field(None, description="URL de la imagen de la categoría")
    parent_id: Optional[int] = Field(None, description="ID de la categoría padre")
    is_active: bool = Field(True, description="Indica si la categoría está activa")
    sort_order: int = Field(0, ge=0, description="Orden de visualización")

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Valida que el slug tenga el formato correcto"""
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('El slug solo puede contener letras minúsculas, números y guiones')
        if v.startswith('-') or v.endswith('-'):
            raise ValueError('El slug no puede empezar o terminar con guión')
        return v

    @field_validator('image_url')
    @classmethod
    def validate_image_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^https?://.+', v):
            raise ValueError('La URL debe comenzar con http:// o https://')
        return v


# Schema para crear una categoría
class CategoryCreateSchema(CategoryBaseSchema):
    """Schema para crear una nueva categoría"""
    pass


# Schema para actualizar una categoría
class CategoryUpdateSchema(BaseModel):
    """Schema para actualizar una categoría existente"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = Field(None, ge=0)

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

    @field_validator('image_url')
    @classmethod
    def validate_image_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^https?://.+\.(jpg|jpeg|png|gif|webp)$', v, re.IGNORECASE):
            raise ValueError('La URL de imagen debe ser válida y terminar en jpg, jpeg, png, gif o webp')
        return v


# Schema básico para respuesta (sin relaciones)
class CategoryResponseSchema(CategoryBaseSchema):
    """Schema básico de respuesta de categoría"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Schema para categoría padre (evita recursión infinita)
class CategoryParentSchema(BaseModel):
    """Schema simplificado para categoría padre"""
    id: int
    name: str
    slug: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


# Schema para categorías hijas (evita recursión infinita)
class CategoryChildSchema(BaseModel):
    """Schema simplificado para categorías hijas"""
    id: int
    name: str
    slug: str
    is_active: bool
    sort_order: int
    
    model_config = ConfigDict(from_attributes=True)


# Schema completo con relaciones
class CategoryDetail(CategoryResponseSchema):
    """Schema detallado con relaciones incluidas"""
    parent: Optional[CategoryParentSchema] = None
    children: List[CategoryChildSchema] = []
    products_count: Optional[int] = Field(None, description="Número de productos en esta categoría")
    
    model_config = ConfigDict(from_attributes=True)


# Schema para listado con paginación
class CategoryList(BaseModel):
    """Schema para listado paginado de categorías"""
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool
    sort_order: int
    created_at: datetime
    products_count: Optional[int] = None
    children_count: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


# Schema para árbol jerárquico (con recursión controlada)
class CategoryTreeSchema(BaseModel):
    """Schema para representar el árbol de categorías"""
    id: int
    name: str
    slug: str
    is_active: bool
    sort_order: int
    children: List['CategoryTreeSchema'] = []
    
    model_config = ConfigDict(from_attributes=True)


# Schema para operaciones de ordenamiento
class CategoryReorderSchema(BaseModel):
    """Schema para reordenar categorías"""
    category_id: int
    new_sort_order: int = Field(ge=0)


# Schema para respuesta de operaciones bulk
class CategoryBulkResponseSchema(BaseModel):
    """Schema para respuestas de operaciones masivas"""
    success: bool
    message: str
    affected_categories: List[int] = []
    errors: List[str] = []


# Schema para filtros de búsqueda
class CategoryFiltersSchema(BaseModel):
    """Schema para filtros de búsqueda de categorías"""
    name: Optional[str] = Field(None, description="Buscar por nombre (contiene)")
    parent_id: Optional[int] = Field(None, description="Filtrar por categoría padre")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    has_products: Optional[bool] = Field(None, description="Solo categorías con/sin productos")
    level: Optional[int] = Field(None, ge=0, description="Nivel en la jerarquía (0=raíz)")


# Schema para respuesta paginada
class CategoryPaginatedResponseSchema(BaseModel):
    """Schema para respuesta paginada"""
    items: List[CategoryList]
    total: int
    page: int = Field(ge=1)
    size: int = Field(ge=1, le=100)
    pages: int
    has_next: bool
    has_prev: bool
    
    model_config = ConfigDict(from_attributes=True)


# Necesario para resolver las referencias hacia adelante en CategoryTree
CategoryTreeSchema.model_rebuild()