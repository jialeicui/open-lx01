from __future__ import annotations

import os
import typing

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

from api.persona import HISTORY_TEACHER
from llm.llm import LLMChat


class Moonshot(LLMChat):
    def __init__(self, api_key: str, prompt: str | None = None, **kwargs: typing.Any):
        super().__init__("moonshot", prompt=prompt, **kwargs)
        self._client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")

    def round(self, text: str, temperature: float) -> ChatCompletionMessage:
        completion = self._client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=self.messages,
            temperature=temperature,
        )

        return completion.choices[0].message


if __name__ == "__main__":
    moonshot = Moonshot(
        prompt=HISTORY_TEACHER, api_key=os.getenv("MOONSHOT_API_KEY") or ""
    )
    print(moonshot.chat("李白平均每年写多少首诗？"))
