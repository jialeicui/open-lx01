from __future__ import annotations

from abc import abstractmethod
from typing import List

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)


class LLMChat:
    def __init__(self, prompt: str = ""):
        self.prompt = prompt
        self.messages: List[ChatCompletionMessageParam] = []
        if prompt:
            self.messages.append(
                ChatCompletionSystemMessageParam(content=prompt, role="system")
            )

    def new_session(self) -> None:
        self.messages = []
        if self.prompt:
            self.messages.append({"role": "system", "content": self.prompt})

    @abstractmethod
    def round(self, text: str, temperature: float) -> ChatCompletionMessage:
        ...

    def chat(self, text: str, temperature: float = 0.3) -> str | None:
        self.messages.append(ChatCompletionUserMessageParam(content=text, role="user"))
        response = self.round(text, temperature)
        self.messages.append(
            ChatCompletionAssistantMessageParam(
                content=response.content, role="assistant"
            )
        )
        return response.content
