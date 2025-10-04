from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

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
    DATABASE_USER_FA: str 
    DATABASE_PASSWORD_FA: str 
    DATABASE_HOST_FA: str 
    DATABASE_NAME_FA: str 
    DATABASE_PORT_FA: int 
    
    # Configuración SMTP
    SMTP_HOST_FA: str 
    SMTP_PORT_FA: int   # 👈 Agregado
    SMTP_USER_FA: str 
    SMTP_PASSWORD_FA: str 
    
    # Configuración JWT
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    
    # Configuración de la aplicación
    APP_NAME: str = "Mi Primera API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    

    @property
    def get_sync_database_url(self) -> str:
        """
        Genera la URL de conexión síncrona para Alembic.
        """
        return f"postgresql+psycopg2://{self.DATABASE_USER_FA}:{self.DATABASE_PASSWORD_FA}@{self.DATABASE_HOST_FA}:{self.DATABASE_PORT_FA}/{self.DATABASE_NAME_FA}"
    
    @property
    def get_async_database_url(self) -> str:
        """
        Genera la URL de conexión asíncrona para la aplicación.
        """
        return f"postgresql+asyncpg://{self.DATABASE_USER_FA}:{self.DATABASE_PASSWORD_FA}@{self.DATABASE_HOST_FA}:{self.DATABASE_PORT_FA}/{self.DATABASE_NAME_FA}"


# Instancia global de configuración
settings = Settings()
