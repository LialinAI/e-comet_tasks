from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class BaseConfig(BaseSettings):

    class Config:
        env_file = BASE_DIR / ".env"


class PostgresConfig(BaseConfig):

    user: str = Field(..., alias="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD")
    db: str = Field(..., alias="POSTGRES_DB")
    host: str = Field("127.0.0.1", alias="DB_HOST")
    port: int = Field(5432, alias="DB_PORT")


pg_config = PostgresConfig()
