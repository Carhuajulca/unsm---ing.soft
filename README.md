# Mi Primera API - FastAPI

API REST moderna construida con FastAPI para gestión de usuarios y productos.

## 🚀 Características

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **PostgreSQL**: Base de datos principal
- **Alembic**: Migraciones de base de datos
- **JWT**: Autenticación con tokens
- **Pydantic**: Validación de datos
- **Arquitectura en capas**: Separación clara de responsabilidades

## 📋 Requisitos

- Python 3.13+
- PostgreSQL
- Pipenv

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd proyecto1
```

### 2. Instalar dependencias
```bash
pipenv install
```

### 3. Configurar variables de entorno
Crear un archivo `.env` basado en el siguiente ejemplo:

```env
# Configuración de Base de Datos
DATABASE_USER_FA=postgres
DATABASE_PASSWORD_FA=your_password_here
DATABASE_HOST_FA=localhost
DATABASE_NAME_FA=fastapi_db
DATABASE_PORT_FA=5432

# Configuración SMTP
SMTP_HOST_FA=smtp.gmail.com
SMTP_PORT_FA=587
SMTP_USER_FA=your_email@gmail.com
SMTP_PASSWORD_FA=your_app_password

# Configuración JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de la Aplicación
APP_NAME=Mi Primera API
APP_VERSION=1.0.0
DEBUG=true
```

### 4. Configurar base de datos
```bash
# Crear base de datos PostgreSQL
createdb fastapi_db

# Ejecutar migraciones
pipenv run alembic upgrade head
```

### 5. Ejecutar la aplicación
```bash
pipenv run uvicorn src.main:app --reload
```

## 📚 Documentación de la API

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticación

La API usa JWT para autenticación. Para obtener un token:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=gesler&password=123456"
```

## 📁 Estructura del Proyecto

```
src/
├── api/v1/           # Endpoints de la API
├── core/             # Configuración y utilidades centrales
├── database.py       # Configuración de base de datos
├── main.py          # Punto de entrada de la aplicación
├── user/            # Módulo de usuarios
│   ├── models/      # Modelos de base de datos
│   ├── repositories/ # Acceso a datos
│   ├── routers/     # Endpoints de la API
│   ├── schemas/     # Esquemas Pydantic
│   └── services/    # Lógica de negocio
├── product/         # Módulo de productos
└── utils/           # Utilidades generales
```

## 🔧 Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión

### Usuarios
- `POST /api/v1/users/register` - Registrar usuario
- `GET /api/v1/users/{user_id}` - Obtener usuario
- `GET /api/v1/users/` - Listar usuarios
- `PUT /api/v1/users/{user_id}` - Actualizar usuario
- `DELETE /api/v1/users/{user_id}/soft` - Soft delete
- `DELETE /api/v1/users/{user_id}/hard` - Hard delete

### Categorías
- `GET /api/v1/categories/` - Listar categorías
- `POST /api/v1/categories/` - Crear categoría

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pipenv run pytest
```

## 🚀 Despliegue

### Desarrollo
```bash
pipenv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
pipenv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📝 Migraciones

```bash
# Crear nueva migración
pipenv run alembic revision --autogenerate -m "descripción"

# Ejecutar migraciones
pipenv run alembic upgrade head

# Revertir migración
pipenv run alembic downgrade -1
```

## 🔒 Seguridad

- Contraseñas hasheadas con bcrypt
- Validación de fortaleza de contraseñas
- Tokens JWT con expiración
- Sanitización de datos de entrada
- Validación de emails

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación de la API en `/docs`
2. Verifica los logs de la aplicación
3. Asegúrate de que todas las variables de entorno estén configuradas
4. Verifica que PostgreSQL esté ejecutándose

## 🔄 Changelog

### v1.0.0
- Implementación inicial de la API
- Sistema de usuarios completo
- Autenticación JWT
- Migraciones con Alembic
- Documentación automática
