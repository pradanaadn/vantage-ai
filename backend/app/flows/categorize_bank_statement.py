from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Tuple
from urllib.parse import unquote, urlparse, parse_qs
import mimetypes

from firebase_admin import storage
from google.genai import types
from loguru import logger
from prefect import flow, task
from prefect.deployments import run_deployment
from app.models.financial import FinancialReport
from app.repositories import firestore_business, firestore_financial
from app.schemas.file_upload import FileUpload
from app.schemas.financial import FinancialReportCreate
from app.flows.firebase_tasks import (
    init_firebase,
    load_gcp_credentials_block,
    verify_firebase_token,
)
from app.services.bank_statement_categorize import (
    analyze_and_categorize_statement_batch,
    check_batch_job_status,
    get_bank_statement_from_batch_result,
)
from app.flows.secret_task import gemini_secret


@task(name="Extract Blob Path")
def extract_blob_path(file_url: str) -> Tuple[str | None, str]:
    parsed = urlparse(file_url)
    if parsed.scheme == "gs":
        return parsed.netloc, parsed.path.lstrip("/")

    if not parsed.netloc:
        raise ValueError("Invalid file URL; missing host.")

    path_parts = parsed.path.strip("/").split("/")
    if "b" in path_parts and "o" in path_parts:
        bucket_index = path_parts.index("b") + 1
        object_index = path_parts.index("o") + 1
        bucket_name = (
            path_parts[bucket_index] if bucket_index < len(path_parts) else None
        )
        object_path = path_parts[object_index] if object_index < len(path_parts) else ""
        if object_path:
            return bucket_name, unquote(object_path)

    query = parse_qs(parsed.query)
    object_name = query.get("name", [""])[0]
    if object_name:
        return None, unquote(object_name)

    raise ValueError("Unsupported Firebase Storage URL format.")

@task(name="Download File from Firebase")
def download_file_from_firebase(file_url: str) -> FileUpload:
    bucket_name, object_path = extract_blob_path(file_url)
    bucket = storage.bucket(bucket_name) if bucket_name else storage.bucket()
    blob = bucket.blob(object_path)
    data = blob.download_as_bytes()
    content_type = blob.content_type or mimetypes.guess_type(blob.name or "")[0]
    filename = Path(blob.name or "bank_statement.pdf").name
    return FileUpload(
        filename=filename,
        content_type=content_type or "application/octet-stream",
        data=data,
    )


@flow(log_prints=True)
def categorize_bank_statement(
    bank_statement_file_url: str,
    bussiness_id: str,
    id_token: str | None = None,
    developer_mode: bool = True,
    gcp_block_name: str | None = "gcp-sa",
):
    try:
        service_account_info = (
            load_gcp_credentials_block(gcp_block_name) if gcp_block_name else None
        )
    except Exception as e:
        logger.error(f"Error loading GCP credentials block: {e}")
        if developer_mode:
            logger.warning("Developer mode enabled, proceeding without GCP credentials.")
            service_account_info = None
        else:
            raise ValueError("Failed to load GCP credentials block.") from e
        
    if not service_account_info and id_token and not developer_mode:
        logger.warning(
            "ID token provided without GCP credentials block. Firebase initialization may fail."
        )
        raise ValueError("GCP credentials block is required when ID token is provided.")
    
    init_firebase(service_account_info.get_secret_value() if service_account_info else None)

    try:
        gemini_api_key = gemini_secret("gemini-api-key")
    except Exception as e:
        logger.error(f"Error retrieving Gemini API key from Prefect Secret: {e}")
        raise
    if id_token:
        verify_firebase_token(id_token)
        
    with open("prompts/bank_statement_classifier.md", "r") as f:
        system_instruction = f.read()
    file_data = download_file_from_firebase(bank_statement_file_url)
    batch_job = analyze_and_categorize_statement_batch(
        bank_statement=file_data,
        system_instruction=system_instruction,
        api_key=gemini_api_key,
    )

    run_deployment(
        "check-batch-result/check-batch-result",
        parameters={
            "batch_job_name": batch_job.name,
            "bank_statement_file_url": bank_statement_file_url,
            "bussiness_id": bussiness_id,
            "gcp_block_name": gcp_block_name,
        },
        timeout=0
    )


@flow(name="check-batch-result",log_prints=True, retries=3, retry_delay_seconds=300)
def check_batch_result(
    batch_job_name: str,
    bank_statement_file_url: str,
    bussiness_id: str,
    gcp_block_name: str | None = "gcp-sa",
    developer_mode: bool = True,

) -> FinancialReport | None:
    try:
        service_account_info = (
            load_gcp_credentials_block(gcp_block_name) if gcp_block_name else None
        )
    except Exception as e:
        logger.error(f"Error loading GCP credentials block: {e}")
        if developer_mode:
            logger.warning("Developer mode enabled, proceeding without GCP credentials.")
            service_account_info = None
        else:
            raise ValueError("Failed to load GCP credentials block.") from e
        
    if not service_account_info and not developer_mode:
        logger.warning(
            "ID token provided without GCP credentials block. Firebase initialization may fail."
        )
        raise ValueError("GCP credentials block is required when ID token is provided.")
    
    init_firebase(service_account_info.get_secret_value() if service_account_info else None)

    try:
        gemini_api_key = gemini_secret("gemini-api-key")
    except Exception as e:
        logger.error(f"Error retrieving Gemini API key from Prefect Secret: {e}")
        raise
    owner_uid = firestore_business.get_business_owner_uid(bussiness_id)
    if not owner_uid:
        logger.error(
            "Missing business owner for financial report creation: %s",
            bussiness_id,
        )
        return None
    try:
        gemini_api_key = gemini_secret("gemini-api-key")
    except Exception as e:
        logger.error(f"Error retrieving Gemini API key from Prefect Secret: {e}")
        raise
    batch_job = check_batch_job_status(batch_job_name, api_key=gemini_api_key)
    if batch_job.state == types.JobState.JOB_STATE_SUCCEEDED:
        bank_statement_data = get_bank_statement_from_batch_result(batch_job)
        generated_at = batch_job.update_time or datetime.now(
            timezone(offset=timedelta(hours=7))
        )
        created_at = batch_job.create_time or datetime.now(
            timezone(offset=timedelta(hours=7))
        )
        financial_report = FinancialReport(
            file_url=bank_statement_file_url,
            bank_statement=bank_statement_data,
            generated_at=generated_at,
            created_at=created_at,
        )
        report_payload = FinancialReportCreate(
            business_id=bussiness_id,
            file_url=bank_statement_file_url,
            bank_statement=bank_statement_data,
            generated_at=generated_at,
            created_at=created_at,
        )
        firestore_financial.create_financial_report(report_payload, owner_uid)
        return financial_report

    if batch_job.state == types.JobState.JOB_STATE_FAILED:
        logger.error("Batch job failed. Please check the logs for more details.")
        return None

    logger.info(f"Batch job is in state: {batch_job.state}. Retrying soon.")
    raise RuntimeError("Batch job not ready.")

if __name__ == "__main__":
    from prefect import serve
    flow_1 = categorize_bank_statement.to_deployment("categorize-bank-statement")
    flow_2 = check_batch_result.to_deployment("check-batch-result")
    serve(flow_1, flow_2)

