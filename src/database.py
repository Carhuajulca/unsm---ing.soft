
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings



engine = create_async_engine(settings.get_database_url, echo=True, future=True, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker( autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

# Esta es la clase base de todos nuestros modelos
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session