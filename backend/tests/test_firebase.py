import pytest
import uuid
from app.infra.firebase import initialize_firebase
from firebase_admin import auth, firestore, storage

@pytest.fixture(scope="session", autouse=True)
def firebase_app():
    """
    Ensures Firebase is initialized for the entire test session.
    Using initialize_firebase() directly ensures we are testing our actual init logic.
    """
    return initialize_firebase()

@pytest.fixture
def auth_client(firebase_app):
    return auth

@pytest.fixture
def db(firebase_app):
    return firestore.client()

@pytest.fixture
def storage_bucket(firebase_app):
    return storage.bucket()

@pytest.fixture
def unique_id():
    return str(uuid.uuid4())[:8]

def test_firebase_initialization(firebase_app):
    """Verifies that the Firebase app is correctly initialized."""
    assert firebase_app is not None
    assert firebase_app.project_id is not None

def test_firebase_auth(auth_client, unique_id):
    email = f"test_{unique_id}@example.com"
    user = auth_client.create_user(email=email, password="password123")
    try:
        assert user.uid is not None
        assert user.email == email
    finally:
        # Cleanup
        auth_client.delete_user(user.uid)

def test_firestore_client(db, unique_id):
    doc_ref = db.collection("pytest_tests").document(f"doc_{unique_id}")
    doc_ref.set({"test": True, "id": unique_id})
    
    try:
        doc = doc_ref.get()
        assert doc.exists
        assert doc.to_dict()["id"] == unique_id
    finally:
        # Cleanup
        doc_ref.delete()

def test_storage_client(storage_bucket, unique_id):
    blob_name = f"pytest_uploads/test_{unique_id}.txt"
    blob = storage_bucket.blob(blob_name)
    content = b"Pytest storage content"
    
    blob.upload_from_string(content, content_type="text/plain")
    try:
        assert blob.exists()
        downloaded = blob.download_as_bytes()
        assert downloaded == content
    finally:
        # Cleanup
        blob.delete()
