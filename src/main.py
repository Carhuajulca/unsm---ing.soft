from fastapi import FastAPI
from src.database import engine, Base
from src.models.model import User
from contextlib import asynccontextmanager
from src.api.v1.users.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # ✅ Funciona con async
    yield


app = FastAPI(title="Mi Primera API", version="1.0.0", lifespan=lifespan)
app.include_router(user_router, prefix="/api/v1/users", tags=["users apis"])



@app.get("/")
async def root():
    return {"message": "¡Hola, FastAPI!"}