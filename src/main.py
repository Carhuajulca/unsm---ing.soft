from fastapi import FastAPI
# from src.database import engine, Base
from src.models.users import User
from contextlib import asynccontextmanager
from src.api.v1.user import router as user_router
from src.core.db_migrations import run_migrations

# Es útil solo en prototipos o pruebas rápidas.
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)  # ✅ Funciona con async
#     yield

# Es el enfoque “profesional” para proyectos que van a producción.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Correr migraciones automáticamente
    run_migrations()
    yield

app = FastAPI(title="Mi Primera API", version="1.0.0", lifespan=lifespan)
app.include_router(user_router, prefix="/api/v1/users", tags=["users apis"])



@app.get("/")
async def root():
    return {"message": "¡Hola, FastAPI!"}