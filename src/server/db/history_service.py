from __future__ import annotations

import abc
import enum
import time

from peewee import Database

from common.config import DataBaseConfig
from db.db import init_db
from db.models.history import History


class MessageRole(enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class HistoryService(abc.ABC):
    @abc.abstractmethod
    def save(self, message: str, role: MessageRole, provider: str) -> None:
        ...

    @abc.abstractmethod
    def get(self, limit: int = 10, offset: int = 0) -> list[History]:
        ...


class HistorySvcDummy(HistoryService):
    def save(self, message: str, role: MessageRole, provider: str) -> None:
        ...

    def get(self, limit: int = 10, offset: int = 0) -> list[History]:
        return []


class HistorySvcDB(HistoryService):
    def __init__(self, db: Database, provider: str):
        self.db = db
        self.provider = provider

    def save(
        self,
        message: str,
        role: MessageRole,
        provider: str | None = None,
        timestamp: int | None = None,
    ) -> None:
        timestamp = timestamp or int(time.time())
        History.create(
            message=message,
            role=role.value,
            provider=provider or self.provider,
            timestamp=timestamp,
        )

    def get(self, limit: int = 10, offset: int = 0) -> list[History]:
        return list(
            History.select()
            .where(History.provider == self.provider)
            .order_by(History.timestamp.desc())
            .limit(limit)
            .offset(offset)
        )


def get_history_svc(config: DataBaseConfig | None) -> HistoryService:
    if config and config.url:
        return HistorySvcDB(init_db(config), "moonshot")
    return HistorySvcDummy()
