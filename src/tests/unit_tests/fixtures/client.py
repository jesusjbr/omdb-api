from unittest import mock
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from core.deps import get_current_user
from repositories.database.session_factory import get_session
from schemas.shared.user_schema import UserData


@pytest.fixture(scope="function")
def mock_session():
    """Fixture to create a mock session"""
    return MagicMock()


@pytest.fixture(scope="function")
def override_session_dependency(mock_session):
    """Fixture to override session dependency"""
    app.dependency_overrides[get_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def fake_regular_user():
    return UserData(username="username", hashed_password="password", is_admin=False)


@pytest.fixture(scope="function")
def fake_admin_user():
    return UserData(username="username", hashed_password="password", is_admin=True)


@pytest.fixture(scope="function")
def override_get_user_regular(fake_regular_user):
    """Fixture to override get_current_user dependency"""
    app.dependency_overrides[get_current_user] = lambda: fake_regular_user
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def override_get_user_admin(fake_admin_user):
    """Fixture to override get_current_user dependency"""
    app.dependency_overrides[get_current_user] = lambda: fake_admin_user
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def fake_client_regular_user(monkeypatch, override_get_user_regular, override_session_dependency):
    """Fixture to create a fake client for testing"""
    mock_populate_data = mock.AsyncMock()
    monkeypatch.setattr("app.main.populate_data", mock_populate_data)
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def fake_client_admin_user(monkeypatch, override_get_user_admin, override_session_dependency):
    """Fixture to create a fake client for testing"""
    mock_populate_data = mock.AsyncMock()
    monkeypatch.setattr("app.main.populate_data", mock_populate_data)
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def fake_client_without_user(monkeypatch, override_session_dependency):
    """Fixture to create a fake client for testing"""
    mock_populate_data = mock.AsyncMock()
    monkeypatch.setattr("app.main.populate_data", mock_populate_data)
    with TestClient(app) as client:
        yield client
