from __future__ import annotations

from peewee import DatabaseProxy
from playhouse.db_url import connect  # type: ignore

from common.config import DataBaseConfig
from db.models.history import History

db = DatabaseProxy()


def init_db(config: DataBaseConfig) -> None:
    global db
    db.initialize(connect(config.url))
    History.bind(db)
    models = [History]
    db.create_tables(models, safe=True)
