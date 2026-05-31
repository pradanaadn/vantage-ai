import os
import firebase_admin
from firebase_admin import credentials
from google.auth.credentials import AnonymousCredentials
from app.core.config import settings

class EmulatorCredential(credentials.Base):
    def get_credential(self):
        return AnonymousCredentials()

def initialize_firebase(service_account_info: dict | None = None):
    if firebase_admin._apps:
        return firebase_admin.get_app()

    if settings.USE_FIREBASE_EMULATORS:
        print("🔧 Initializing Firebase in EMULATOR mode")
        os.environ["GCLOUD_PROJECT"] = settings.FIREBASE_PROJECT_ID
        os.environ["FIRESTORE_EMULATOR_HOST"] = settings.FIRESTORE_EMULATOR_HOST
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = settings.FIREBASE_AUTH_EMULATOR_HOST
        os.environ["STORAGE_EMULATOR_HOST"] = f"http://{settings.FIREBASE_STORAGE_EMULATOR_HOST}"
        
        cred = EmulatorCredential()
    else:
        print("🚀 Initializing Firebase in PRODUCTION mode")
        if service_account_info:
            cred = credentials.Certificate(service_account_info)
        elif settings.FIREBASE_SERVICE_ACCOUNT_PATH:
            cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
        else:
            # Uses Application Default Credentials
            cred = credentials.ApplicationDefault()

    app_options = {"projectId": settings.FIREBASE_PROJECT_ID}
    if settings.FIREBASE_STORAGE_BUCKET:
        app_options["storageBucket"] = settings.FIREBASE_STORAGE_BUCKET
    elif settings.USE_FIREBASE_EMULATORS:
        app_options["storageBucket"] = f"{settings.FIREBASE_PROJECT_ID}.appspot.com"

    return firebase_admin.initialize_app(cred, options=app_options)
