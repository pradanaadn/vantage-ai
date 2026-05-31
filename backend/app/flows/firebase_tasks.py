from firebase_admin import auth as firebase_auth
from prefect import task
from prefect_gcp import GcpCredentials
from prefect.types import SecretDict

from app.infra.firebase import initialize_firebase


@task(name="Initialize Firebase")
def init_firebase(service_account_info: dict | None = None) -> bool:
    app = initialize_firebase(service_account_info=service_account_info)
    if not app:
        raise RuntimeError("Failed to initialize Firebase app.")
    return app is not None


@task(name="Load GCP Credentials Block")
def load_gcp_credentials_block(block_name: str) -> SecretDict | None:
    gcp_credentials = GcpCredentials.load(block_name)
    print(f"Loaded GCP credentials block '{block_name}' successfully")
    if not isinstance(gcp_credentials, GcpCredentials):
        return None
    if not gcp_credentials.service_account_info:
        raise ValueError("GCP credentials block has no service_account_info")
    return gcp_credentials.service_account_info


@task(name="Verify Firebase Token")
def verify_firebase_token(id_token: str) -> dict:
    initialize_firebase()
    return firebase_auth.verify_id_token(id_token)


if __name__ == "__main__":
    # Example usage for testing
    data = load_gcp_credentials_block("gcp-sa")
    if not data:
        print("Failed to load GCP credentials block.")
    else:
        init_firebase(data.get_secret_value())
        print("Firebase initialized successfully with provided GCP credentials block.")
