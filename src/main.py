from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.user.routers.user_router import router as user_router
from src.user.routers.auth_router import router as auth_router
from src.product.routers.category_router import router as category_router
from src.core.db_migrations import run_migrations

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor del ciclo de vida de la aplicación.
    Ejecuta migraciones automáticamente al iniciar.
    """
    # 🚀 Correr migraciones automáticamente
    run_migrations()
    yield

app = FastAPI(
    title="Mi Primera API", 
    version="1.0.0", 
    lifespan=lifespan,
    description="API REST con FastAPI para gestión de usuarios y productos",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir routers
app.include_router(auth_router, prefix="/api/v1", tags=["authentication"])
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(category_router, prefix="/api/v1/categories", tags=["categories"])

@app.get("/")
async def root():
    """
    Endpoint raíz de la API.
    
    Returns:
        dict: Mensaje de bienvenida
    """
    return {
        "message": "¡Hola, FastAPI!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud de la API.
    
    Returns:
        dict: Estado de la aplicación
    """
    return {
        "status": "healthy",
        "timestamp": "2025-08-23T19:13:00Z"
    }