from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Configuración de la aplicación usando variables de entorno.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='allow'
    )

    # Configuración de base de datos
    DATABASE_USER_FA: str = "postgres"
    DATABASE_PASSWORD_FA: str = "password"
    DATABASE_HOST_FA: str = "localhost"
    DATABASE_NAME_FA: str = "fastapi_db"
    DATABASE_PORT_FA: int = 5432
    
    # Configuración SMTP
    SMTP_HOST_FA: str = "smtp.gmail.com"
    SMTP_PORT_FA: int = 587
    SMTP_USER_FA: str = ""
    SMTP_PASSWORD_FA: str = ""
    
    # Configuración JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de la aplicación
    APP_NAME: str = "Mi Primera API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    @property
    def get_database_url(self) -> str:
        """
        Genera la URL de conexión a la base de datos.
        
        Returns:
            str: URL de conexión PostgreSQL
        """
        return f"postgresql+asyncpg://{self.DATABASE_USER_FA}:{self.DATABASE_PASSWORD_FA}@{self.DATABASE_HOST_FA}:{self.DATABASE_PORT_FA}/{self.DATABASE_NAME_FA}"
    
    @property
    def get_sync_database_url(self) -> str:
        """
        Genera la URL de conexión síncrona para Alembic.
        
        Returns:
            str: URL de conexión PostgreSQL síncrona
        """
        return f"postgresql://{self.DATABASE_USER_FA}:{self.DATABASE_PASSWORD_FA}@{self.DATABASE_HOST_FA}:{self.DATABASE_PORT_FA}/{self.DATABASE_NAME_FA}"

# Instancia global de configuración
settings = Settings()



