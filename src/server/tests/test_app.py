from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app import app as main_app
from db.history_service import MessageRole
from db.models.history import History


@patch("app.get_history_svc")
def test_history(mock_get_history_svc: MagicMock):
    client = TestClient(main_app)
    mock_hv = MagicMock()
    mock_hv.get.return_value = [
        History(
            id=1,
            message="foo",
            role=MessageRole.USER,
            timestamp=2,
            provider="bar",
        )
    ]
    mock_get_history_svc.return_value = mock_hv
    resp = client.get("/history")
    assert resp.status_code == 200
    history = resp.json()
    assert history == [
        {"id": 1, "message": "foo", "role": "user", "timestamp": 2, "provider": "bar"}
    ]
