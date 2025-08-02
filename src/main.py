from fastapi import FastAPI
from src.database import engine, Base
from src.models.model import User
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # ✅ Funciona con async
    yield


app = FastAPI(title="Mi Primera API", version="1.0.0", lifespan=lifespan)

# Ruta básica
@app.get("/")
async def root():
    return {"mensaje": "¡Hola FastAPI!"}