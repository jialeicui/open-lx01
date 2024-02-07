import os
import typing

from pydantic import BaseModel


class DataBaseConfig(BaseModel):
    url: str


class LLMConfig(BaseModel):
    prompt: typing.Optional[str] = ""


class GithubCopilotConfig(LLMConfig):
    api_key: str


class MoonshotConfig(LLMConfig):
    token: str


class Config(BaseModel):
    db: typing.Optional[DataBaseConfig] = None
    llm: typing.Union[GithubCopilotConfig, MoonshotConfig]


def load_config() -> Config:
    return Config(
        db=DataBaseConfig(url="sqlite:///db.sqlite3"),
        llm=MoonshotConfig(token=os.getenv("MOONSHOT_API_KEY") or ""),
    )
