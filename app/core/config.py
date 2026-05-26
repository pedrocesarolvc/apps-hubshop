#guarda o jwt_secrets e outras configs
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'sqlite:///./shophub.db'

    JWT_SECRET: str = 'DOHVnT5S2e-KMO2xZy7xbozIIFfSOdzlxWxx3mjkpOg'
    ALGORITHM: str = 'HS256'

    # 60 minutos * 24 horas * 1 dia
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1

    class Config:
        case_sensitive = True

settings: Settings = Settings()