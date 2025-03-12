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


class GitConfig(BaseConfig):

    model_config = SettingsConfigDict(extra="ignore")

    github_token: str = Field(..., alias="ACCESS_TOKEN")


git_config = GitConfig()
app_config = AppConfig()
