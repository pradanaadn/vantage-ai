from firebase_admin import auth as firebase_auth
from prefect import task
from prefect_gcp import GcpCredentials
from prefect.types import SecretDict

from app.infra.firebase import initialize_firebase


@task(name="Initialize Firebase")
def init_firebase(service_account_info: dict | None = None) -> None:
    initialize_firebase(service_account_info=service_account_info)


@task(name="Load GCP Credentials Block")
def load_gcp_credentials_block(block_name: str) -> SecretDict:
    gcp_credentials = GcpCredentials.load(block_name)
    if not isinstance(gcp_credentials, GcpCredentials):
        raise ValueError(
            f"GCP credentials block '{block_name}' has no service_account_info"
        )
    if not gcp_credentials.service_account_info:
        raise ValueError("GCP credentials block has no service_account_info")
    return gcp_credentials.service_account_info


@task(name="Verify Firebase Token")
def verify_firebase_token(id_token: str) -> dict:
    initialize_firebase()
    return firebase_auth.verify_id_token(id_token)
