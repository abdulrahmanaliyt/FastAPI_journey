from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "postgresql+psycopg://postgres:1234@localhost:5433/StudentCourseApp"
    class Config:
        env_file = ".env"

settings = Settings()