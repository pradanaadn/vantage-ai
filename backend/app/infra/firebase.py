import os
import uuid

# 1. FORCE EMULATOR ENVIRONMENT (Must be done before ANY firebase imports)
os.environ["GCLOUD_PROJECT"] = "demo-project"
os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "127.0.0.1:9099"
os.environ["STORAGE_EMULATOR_HOST"] = "http://127.0.0.1:9199"

import firebase_admin
from firebase_admin import auth, firestore, storage, credentials
from google.auth.credentials import AnonymousCredentials

# 🔥 THE CLEAN FIX: Create a standard Firebase credential that returns Anonymous Auth
class EmulatorCredential(credentials.Base):
    def get_credential(self):
        return AnonymousCredentials()

def run_emulator_diagnostic():
    print("🚀 Starting Firebase Emulator Suite verification diagnostics...")
    
    # Initialize basic Firebase App using the Anonymous Credential
    app = firebase_admin.initialize_app(EmulatorCredential(), options={
        "projectId": os.environ["GCLOUD_PROJECT"],
        "storageBucket": f"{os.environ['GCLOUD_PROJECT']}.appspot.com"
    })
    
    print("🔧 App initialized with Anonymous Credentials to bypass live OAuth.")

    unique_id = str(uuid.uuid4())[:8]
    print("-" * 50)

    # -------------------------------------------------------------------------
    # TEST 1: AUTHENTICATION
    # -------------------------------------------------------------------------
    try:
        print("1️⃣ Testing Authentication Emulator...")
        user = auth.create_user(email=f"test_{unique_id}@example.com", password="password123")
        print(f"   ✅ SUCCESS: Created user! UID: {user.uid}")
        auth.delete_user(user.uid)
        print("   🧹 Cleaned up emulated user record.")
    except Exception as e:
        print(f"   ❌ FAILED: Auth failed: {e}")

    print("-" * 50)

    # -------------------------------------------------------------------------
    # TEST 2: FIRESTORE
    # -------------------------------------------------------------------------
    try:
        print("2️⃣ Testing Firestore Emulator...")
        db = firestore.client()
        doc_ref = db.collection("emulator_tests").document(f"doc_{unique_id}")
        doc_ref.set({"version": 2026, "status": "connected"})
        print(f"   ✅ SUCCESS: Document written: {doc_ref.path}")
        doc_ref.delete()
        print("   🧹 Cleaned up Firestore doc.")
    except Exception as e:
        print(f"   ❌ FAILED: Firestore failed: {e}")

    print("-" * 50)

    # -------------------------------------------------------------------------
    # TEST 3: CLOUD STORAGE
    # -------------------------------------------------------------------------
    try:
        print("3️⃣ Testing Storage Emulator...")
        bucket = storage.bucket()
        blob = bucket.blob(f"test_uploads/diagnostic_{unique_id}.txt")
        
        # Try uploading data
        blob.upload_from_string("Emulator test content", content_type="text/plain")
        print(f"   ✅ SUCCESS: Uploaded blob to emulator: {blob.name}")
        
        # Try downloading data
        data = blob.download_as_bytes()
        print(f"   ✅ SUCCESS: Downloaded data successfully ({len(data)} bytes)")
        
        # Cleanup
        # blob.delete()
        print("   🧹 Cleaned up Storage test blob.")
    except Exception as e:
        print(f"   ❌ FAILED: Cloud Storage integration failed. Error: {e}")

    print("-" * 50)

if __name__ == "__main__":
    run_emulator_diagnostic()