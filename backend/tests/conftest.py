import pytest
from app.infra.firebase import initialize_firebase

@pytest.fixture(scope="session", autouse=True)
def firebase_app():
    """
    Ensures Firebase is initialized for the entire test session.
    """
    return initialize_firebase()
