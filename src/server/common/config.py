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


class AzureTTSConfig(BaseModel):
    subscription_key: str
    region: str
    voice: str = "en-US-JessaNeural"
    output_format: str = "riff-24khz-16bit-mono-pcm"


class Config(BaseModel):
    db: typing.Optional[DataBaseConfig] = None
    llm: typing.Union[GithubCopilotConfig, MoonshotConfig]
    azure_tts: typing.Optional[AzureTTSConfig] = None


def load_config() -> Config:
    azure_tts_config = None
    if os.getenv("AZURE_TTS_SUBSCRIPTION_KEY") and os.getenv("AZURE_TTS_REGION"):
        azure_tts_config = AzureTTSConfig(
            subscription_key=os.getenv("AZURE_TTS_SUBSCRIPTION_KEY", ""),
            region=os.getenv("AZURE_TTS_REGION", ""),
            voice=os.getenv("AZURE_TTS_VOICE", "en-US-JessaNeural"),
            output_format=os.getenv(
                "AZURE_TTS_OUTPUT_FORMAT", "riff-24khz-16bit-mono-pcm"
            ),
        )

    return Config(
        db=DataBaseConfig(url="sqlite:///db.sqlite3"),
        llm=MoonshotConfig(token=os.getenv("MOONSHOT_API_KEY") or ""),
        azure_tts=azure_tts_config,
    )
