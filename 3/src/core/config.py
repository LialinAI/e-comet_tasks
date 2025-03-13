from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class BaseConfig(BaseSettings):

    class Config:
        env_file = BASE_DIR / ".env"


class AppConfig(BaseConfig):

    model_config = SettingsConfigDict(extra="ignore")

    mcr: int = Field(20, alias="MCR")
    rps: int = Field(20, alias="RPS")
    batch_size: int = Field(20, alias="BATCH_SIZE")


class GitConfig(BaseConfig):

    model_config = SettingsConfigDict(extra="ignore")

    github_token: str = Field(..., alias="ACCESS_TOKEN")


class ClickhouseConfig(BaseConfig):

    model_config = SettingsConfigDict(extra="ignore")

    user: str = Field(..., alias="CLICKHOUSE_USER")
    password: str = Field(..., alias="CLICKHOUSE_PASSWORD")
    db: str = Field(..., alias="CLICKHOUSE_DB")
    host: str = Field(..., alias="CLICKHOUSE_HOST")
    port: str = Field(..., alias="CLICKHOUSE_PORT")

    @property
    def url(self) -> str:
        return (
            f"http://{self.host}:{self.port}/"
        )


git_config = GitConfig()
app_config = AppConfig()
clickhouse_config = ClickhouseConfig()