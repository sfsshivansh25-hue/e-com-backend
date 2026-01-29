from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ecommerce-api"
    ENV: str = "dev"

    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()