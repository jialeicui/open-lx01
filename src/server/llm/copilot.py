from __future__ import annotations

import json
import os

import requests


class GithubCopilot:
    """Github Copilot API"""

    def __init__(self, api_key: str | None = None, prompt: str = ""):
        if api_key is None:
            api_key = self.get_host_key()
        self.api_key = api_key
        self.auth_token = self.get_auth_token()
        self.messages = []
        if prompt:
            self.messages.append({"role": "system", "content": prompt})
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
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

    @staticmethod
    def random_hex(len: int) -> str:
        import random

        return "".join([random.choice("0123456789ABCDEF") for x in range(len)])

    @staticmethod
    def get_host_key() -> str:
        path = os.getenv("HOME") + "/.config/github-copilot/hosts.json"
        with open(path, "r") as f:
            content = json.load(f)
            return content["github.com"]["oauth_token"]

    def get_auth_token(self) -> str:
        url = "https://api.github.com/copilot_internal/v2/token"
        headers = {
            "Authorization": f"token {self.api_key}",
        }
        response = requests.get(url, headers=headers).json()
        return response["token"]

    def chat(self, content: str, temperature: float = 0.5) -> str:
        """Get code from Github Copilot API"""
        url = "https://api.githubcopilot.com/chat/completions"
        self.messages.append({"role": "user", "content": content})
        data = {
            "messages": self.messages,
            "model": "gpt-4",
            "temperature": temperature,
            "top_p": 1,
            "n": 1,
            "stream": False,
        }
        response = requests.post(url, headers=self.headers, json=data).json()
        msg = response["choices"][0]["message"]
        self.messages.append(msg)
        return msg["content"]


if __name__ == "__main__":
    prompt = """# Character
You are an experienced programmer from the United States with proficiency in both English and Chinese. Here, you are required to translate Chinese description into succinct English when submitting the code.

## Skills
### Skill 1: Chinese to English translation
- Carefully read and understand the Chinese description provided.
- Make a concise, yet comprehensive English translation of the Chinese content.
- Ensure that the translated content maintains the original meaning and intent of the Chinese description.

### Skill 2: Submitting code 
- Assist in the code submission process, making sure all the requirements are met.
- Ensure the English descriptions submitted with the code are properly formatted and comply with the set guidelines.

## Constraints:
- Only handle tasks regarding translating Chinese descriptions to English and code submission.
- Always respond in the language used by the user.
- Only use the language that the original prompt uses. 
- Start your response with the translated description directly.
"""
    copilot = GithubCopilot(prompt=prompt)
    print(copilot.chat("我是一个语言模型，我的回答是基于我在训练过程中接触到的数据"))
