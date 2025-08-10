from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra='allow'
    )

    DATABASE_USER_FA: str 
    DATABASE_PASSWORD_FA: str
    DATABASE_HOST_FA: str
    DATABASE_NAME_FA: str 
    SMTP_HOST_FA: str
    SMTP_PORT_FA: int 
    SMTP_USER_FA: str
    SMTP_PASSWORD_FA: str 
    
    @property
    def get_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USER_FA}:{self.DATABASE_PASSWORD_FA}@{self.DATABASE_HOST_FA}/{self.DATABASE_NAME_FA}"



settings = Settings()



