from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Tuple
from urllib.parse import unquote, urlparse, parse_qs
import mimetypes

from firebase_admin import storage
from google.genai import types
from loguru import logger
from prefect import flow
from prefect.deployments import run_deployment

from app.infra.firebase import initialize_firebase
from app.models.financial import FinancialReport
from app.repositories import firestore_financial
from app.schemas.file_upload import FileUpload
from app.schemas.financial import FinancialReportCreate
from app.services.bank_statement_categorize import (
    analyze_and_categorize_statement_batch,
    check_batch_job_status,
    get_bank_statement_from_batch_result,
)


def _extract_blob_path(file_url: str) -> Tuple[str | None, str]:
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


def _download_file_from_firebase(file_url: str) -> FileUpload:
    bucket_name, object_path = _extract_blob_path(file_url)
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
def categorize_bank_statement(bank_statement_file_url: str, bussiness_id: str):
    initialize_firebase()
    file_data = _download_file_from_firebase(bank_statement_file_url)
    batch_job = analyze_and_categorize_statement_batch(
        bank_statement=file_data,
        system_instruction="Extract and categorize the data from this bank statement.",
    )

    run_deployment(
        "check_batch_job_status",
        parameters={
            "batch_job_name": batch_job.name,
            "bank_statement_file_url": bank_statement_file_url,
            "bussiness_id": bussiness_id,
        },
    )


@flow(log_prints=True, retries=3, retry_delay_seconds=15)
def check_batch_result(
    batch_job_name: str,
    bank_statement_file_url: str,
    bussiness_id: str,
) -> FinancialReport | None:
    initialize_firebase()
    batch_job = check_batch_job_status(batch_job_name)
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
        firestore_financial.create_financial_report(report_payload)
        return financial_report

    if batch_job.state == types.JobState.JOB_STATE_FAILED:
        logger.error("Batch job failed. Please check the logs for more details.")
        return None

    logger.info(f"Batch job is in state: {batch_job.state}. Retrying soon.")
    raise RuntimeError("Batch job not ready.")
