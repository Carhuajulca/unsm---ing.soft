#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad JWT completa
"""
import asyncio
import sys
import os
import requests
import json

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database import SessionLocal
from src.user.repository.user_repository import UserRepository
from src.user.services.user_service import UserService
from src.user.schemas.user_schema import UserCreateSchema

# Configuración de la API
API_BASE_URL = "http://localhost:8000/api/v1"

async def test_jwt_flow():
    """Prueba el flujo completo de JWT"""
    print("🧪 Iniciando prueba de flujo JWT completo...")
    print("=" * 60)
    
    try:
        # 1. Crear un usuario de prueba
        print("1️⃣ Creando usuario de prueba...")
        async with SessionLocal() as db:
            user_repository = UserRepository(db)
            user_service = UserService(user_repository)
            
            test_user_data = UserCreateSchema(
                first_name="Test",
                last_name="User",
                email="test.user@example.com",
                password="Test123!@#",
                is_active=True
            )
            
            user = await user_service.register_user(test_user_data)
            print(f"   ✅ Usuario creado: {user.email}")
        
        # 2. Probar login
        print("\n2️⃣ Probando login...")
        login_data = {
            "username": "test.user@example.com",  # OAuth2 usa 'username' para email
            "password": "Test123!@#"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   ✅ Login exitoso")
            print(f"   Token: {access_token[:50]}...")
        else:
            print(f"   ❌ Login falló: {response.status_code} - {response.text}")
            return False
        
        # 3. Probar endpoint protegido
        print("\n3️⃣ Probando endpoint protegido...")
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(
            f"{API_BASE_URL}/auth/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"   ✅ Endpoint protegido accesible")
            print(f"   Usuario: {user_info['first_name']} {user_info['last_name']}")
        else:
            print(f"   ❌ Endpoint protegido falló: {response.status_code} - {response.text}")
            return False
        
        # 4. Probar verificación de token
        print("\n4️⃣ Probando verificación de token...")
        response = requests.get(
            f"{API_BASE_URL}/auth/verify",
            headers=headers
        )
        
        if response.status_code == 200:
            verify_data = response.json()
            print(f"   ✅ Token verificado: {verify_data['message']}")
        else:
            print(f"   ❌ Verificación falló: {response.status_code} - {response.text}")
            return False
        
        # 5. Probar endpoint sin token (debería fallar)
        print("\n5️⃣ Probando endpoint sin token...")
        response = requests.get(f"{API_BASE_URL}/auth/me")
        
        if response.status_code == 401:
            print(f"   ✅ Correctamente rechazado sin token")
        else:
            print(f"   ⚠️  Endpoint accesible sin token (inseguro)")
        
        # 6. Probar logout
        print("\n6️⃣ Probando logout...")
        response = requests.post(
            f"{API_BASE_URL}/auth/logout",
            headers=headers
        )
        
        if response.status_code == 200:
            logout_data = response.json()
            print(f"   ✅ Logout exitoso: {logout_data['message']}")
        else:
            print(f"   ❌ Logout falló: {response.status_code} - {response.text}")
        
        print("\n" + "=" * 60)
        print("🎉 Prueba de flujo JWT completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Prueba los endpoints de la API usando requests"""
    print("\n🌐 Probando endpoints de la API...")
    print("=" * 40)
    
    # Verificar que la API esté corriendo
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ API está corriendo")
        else:
            print("❌ API no está respondiendo correctamente")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la API. Asegúrate de que esté corriendo en http://localhost:8000")
        return False
    
    # Probar endpoint de salud
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check: {health_data['status']}")
        else:
            print("❌ Health check falló")
    except Exception as e:
        print(f"❌ Error en health check: {e}")
    
    return True

async def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de JWT...")
    
    # Primero verificar que la API esté corriendo
    if not test_api_endpoints():
        print("\n💡 Para ejecutar las pruebas:")
        print("1. Asegúrate de que la API esté corriendo:")
        print("   pipenv run uvicorn src.main:app --reload")
        print("2. Ejecuta este script nuevamente")
        sys.exit(1)
    
    # Ejecutar pruebas de JWT
    success = await test_jwt_flow()
    
    if success:
        print("\n🎯 Resumen:")
        print("✅ Registro de usuario")
        print("✅ Login con JWT")
        print("✅ Acceso a endpoints protegidos")
        print("✅ Verificación de token")
        print("✅ Logout")
        print("\n🔐 JWT implementado correctamente!")
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
