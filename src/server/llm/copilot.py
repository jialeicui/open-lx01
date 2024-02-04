from __future__ import annotations

import json
import os
import typing

import requests
from openai.types.chat import ChatCompletionMessage

from api.persona import HISTORY_TEACHER
from llm.llm import LLMChat


class GithubCopilot(LLMChat):
    """Github Copilot API"""

    def __init__(
        self,
        api_key: str | None = None,
        prompt: str | None = None,
        **kwargs: typing.Any,
    ):
        if api_key is None:
            api_key = self.get_host_key()
        self.api_key = api_key
        super().__init__("github", prompt=prompt, **kwargs)

        self.headers = {
            "User-Agent": "GitHubCopilotChat/0.8.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate,br",
            "Content-Type": "application/json; charset=utf-8",
            "Openai-Intent": "conversation-panel",
            "Openai-Organization": "github-copilot",
            "Editor-Plugin-Version": "copilot-chat/0.8.0",
            "Editor-Version": "vscode/1.83.1",
            "Vscode-Machineid": self.random_hex(64),
            "Vscode-Sessionid": "-".join(
                [self.random_hex(i) for i in [8, 4, 4, 4, 25]]
            ),
            "X-Request-Id": "-".join([self.random_hex(i) for i in [8, 4, 4, 4, 12]]),
        }
        self._refresh_auth_token()

    @staticmethod
    def random_hex(len: int) -> str:
        import random

        return "".join([random.choice("0123456789ABCDEF") for x in range(len)])

    @staticmethod
    def get_host_key() -> str:
        home = os.getenv("HOME")
        assert home is not None
        path = home + "/.config/github-copilot/hosts.json"
        with open(path, "r") as f:
            content = json.load(f)
            return content["github.com"]["oauth_token"]

    def new_session(self) -> None:
        self.messages = []

    def get_auth_token(self) -> str:
        url = "https://api.github.com/copilot_internal/v2/token"
        headers = {
            "Authorization": f"token {self.api_key}",
        }
        response = requests.get(url, headers=headers).json()
        return response["token"]

    def _refresh_auth_token(self) -> None:
        token = self.get_auth_token()
        self.headers["Authorization"] = f"Bearer {token}"

    def round(self, content: str, temperature: float) -> ChatCompletionMessage:
        """Get code from Github Copilot API"""
        url = "https://api.githubcopilot.com/chat/completions"
        data = {
            "messages": self.messages,
            "model": "gpt-4",
            "temperature": temperature,
            "top_p": 1,
            "n": 1,
            "stream": False,
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 401:
            self._refresh_auth_token()
            response = requests.post(url, headers=self.headers, json=data)
        msg = response.json()["choices"][0]["message"]
        return ChatCompletionMessage(content=msg["content"], role="assistant")


if __name__ == "__main__":
    copilot = GithubCopilot(prompt=HISTORY_TEACHER)
    print(copilot.chat("李白平均每年写多少首诗？"))
