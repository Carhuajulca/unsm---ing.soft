#!/usr/bin/env python3
"""
Script de prueba para verificar la creación de usuarios
"""
import asyncio
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database import SessionLocal
from src.user.repository.user_repository import UserRepository
from src.user.services.user_service import UserService
from src.user.schemas.user_schema import UserCreateSchema

async def test_user_creation():
    """Prueba la creación de un usuario"""
    try:
        # Crear sesión de base de datos
        async with SessionLocal() as db:
            # Crear repositorio y servicio
            user_repository = UserRepository(db)
            user_service = UserService(user_repository)
            
            # Datos de prueba
            test_user_data = UserCreateSchema(
                first_name="Juan",
                last_name="Pérez",
                email="juan.perez@test.com",
                password="Test123!@#",
                is_active=True
            )
            
            print("🔄 Intentando crear usuario...")
            
            # Crear usuario
            user = await user_service.register_user(test_user_data)
            
            print("✅ Usuario creado exitosamente!")
            print(f"   ID: {user.id}")
            print(f"   Nombre: {user.first_name} {user.last_name}")
            print(f"   Email: {user.email}")
            print(f"   Activo: {user.is_active}")
            print(f"   Creado: {user.created_at}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al crear usuario: {str(e)}")
        print(f"   Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Función principal"""
    print("🧪 Iniciando prueba de creación de usuario...")
    print("=" * 50)
    
    success = await test_user_creation()
    
    print("=" * 50)
    if success:
        print("🎉 Prueba completada exitosamente!")
    else:
        print("💥 Prueba falló!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
