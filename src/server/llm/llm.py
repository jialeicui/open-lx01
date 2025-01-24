from __future__ import annotations

import typing
from abc import abstractmethod
from typing import List

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from db.history_service import HistoryService, MessageRole


class LLMChat:
    def __init__(self, provider: str, prompt: str | None = None, **kwargs: typing.Any):
        self.provider = provider
        self.prompt = prompt or ""
        self.history_svc: HistoryService | None = kwargs.get("history_svc", None)
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
    def round(self, text: str, temperature: float) -> ChatCompletionMessage: ...

    def _save_message(self, message: str | None, role: MessageRole) -> None:
        if message is None:
            return
        if self.history_svc:
            self.history_svc.save(
                message=message,
                role=role,
                provider=role == MessageRole.USER and "" or self.provider,
            )

    def chat(self, text: str, temperature: float = 0.3) -> str | None:
        self.messages.append(ChatCompletionUserMessageParam(content=text, role="user"))
        response = self.round(text, temperature)
        self.messages.append(
            ChatCompletionAssistantMessageParam(
                content=response.content, role="assistant"
            )
        )
        self._save_message(message=text, role=MessageRole.USER)
        self._save_message(message=response.content, role=MessageRole.ASSISTANT)

        return response.content
