from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users.user import UserCreate
from src.database import get_db
from src.models.model import User
from sqlalchemy import select

router = APIRouter()

@router.post("/user_create", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Debug: Imprime los atributos disponibles del modelo User
    print("Atributos de User:", dir(User))

    # Verificar si el email ya existe
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el username ya existe
    result = await db.execute(select(User).where(User.name == user.username))
    existing_username = result.scalar_one_or_none()
    
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    # Crear el usuario
    db_user = User(
        name=user.username,
        email=user.email,
        is_active=user.is_active
    )
    
    db.add(db_user)
    await db.commit()  # await es crucial en async
    
    return {"message": "Usuario creado exitosamente"}