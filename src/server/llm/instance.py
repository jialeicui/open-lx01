from common.config import Config, GithubCopilotConfig, MoonshotConfig
from db.history_service import get_history_svc
from llm.copilot import GithubCopilot
from llm.llm import LLMChat
from llm.moonshot import Moonshot


def get_llm(config: Config) -> LLMChat:
    history_svc = get_history_svc(config.db)

    if isinstance(config.llm, GithubCopilotConfig):
        return GithubCopilot(
            api_key=config.llm.api_key,
            prompt=config.llm.prompt,
            history_svc=history_svc,
        )
    elif isinstance(config.llm, MoonshotConfig):
        return Moonshot(
            api_key=config.llm.token, prompt=config.llm.prompt, history_svc=history_svc
        )
    else:
        raise ValueError("Invalid LLM config")
