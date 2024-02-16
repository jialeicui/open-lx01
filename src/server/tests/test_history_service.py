from pathlib import Path
from unittest import TestCase

from common.config import DataBaseConfig
from db.history_service import HistorySvcDummy, MessageRole, get_history_svc


class TestHistorySvcDB(TestCase):
    def setUp(self):
        # make sure db not exits
        self.db_file = f"{self.__class__.__name__}.sqlite3"
        self.remove_file(self.db_file)

    def tearDown(self):
        self.remove_file(self.db_file)

    @staticmethod
    def remove_file(file: str) -> None:
        Path(file).unlink(missing_ok=True)

    def test_save(self):
        svc = get_history_svc(None)
        assert isinstance(svc, HistorySvcDummy)

        config: DataBaseConfig = DataBaseConfig(url=f"sqlite:///{self.db_file}")
        svc = get_history_svc(config)
        svc.save("message", MessageRole.USER, "moonshot")

        history = svc.get()
        assert len(history) == 1
        assert history[0].message == "message"
        assert history[0].role == "user"
        assert history[0].provider == "moonshot"
        assert history[0].timestamp is not None
        assert history[0].id is not None
