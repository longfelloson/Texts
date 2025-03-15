from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class AuthConfig(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str


class DatabaseConfig(BaseSettings):
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str
    DB_PASSWORD: str
    DB_USER: str

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    

class Settings(DatabaseConfig, AuthConfig):
    ...


settings = Settings()
