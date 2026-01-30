from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ecommerce-api"
    ENV: str = "dev"
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    SMTP_FROM: str
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
    


settings = Settings()


