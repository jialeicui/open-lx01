from unittest import TestCase

from common.config import DataBaseConfig
from db.history_service import HistorySvcDummy, MessageRole, get_history_svc


class TestHistorySvcDB(TestCase):
    def test_save(self):
        svc = get_history_svc(None)
        assert isinstance(svc, HistorySvcDummy)

        config: DataBaseConfig = DataBaseConfig(url="sqlite:///:memory:")
        svc = get_history_svc(config)
        svc.save("message", MessageRole.USER, "moonshot")

        history = svc.get()
        assert len(history) == 1
        assert history[0].message == "message"
        assert history[0].role == "user"
        assert history[0].provider == "moonshot"
        assert history[0].timestamp is not None
        assert history[0].id is not None

