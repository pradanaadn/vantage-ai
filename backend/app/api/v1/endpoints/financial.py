from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from app.schemas.financial import (
    BankStatementCategorizeResponse,
    BankStatementUploadRequest,
    BankStatementUploadResponse,
    FinancialReportInDB,
)
from app.services import financial_service
from firebase_admin import storage
from uuid import uuid4
from prefect.deployments import arun_deployment

router = APIRouter()


@router.post("/bank-statement/extract", status_code=status.HTTP_201_CREATED)
async def extract_and_categorize_bank_statement(
    payload: BankStatementUploadRequest,
) -> BankStatementCategorizeResponse:
    flow_run = await arun_deployment(
        "categorize-bank-statement",
        parameters={
            "bank_statement_file_url": payload.file_url,
            "bussiness_id": payload.business_id,
        },
    )
    if not flow_run:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start bank statement categorization flow.",
        )
    if not flow_run.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Flow run did not return a valid ID.",
        )
    return BankStatementCategorizeResponse(flow_run_id=str(flow_run.id))


@router.post("/bank-statement/upload", status_code=status.HTTP_201_CREATED)
async def upload_bank_statement_file(
    business_id: str = Form(...),
    file: UploadFile = File(...),
) -> BankStatementUploadResponse:
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only PDF files are allowed.",
        )

    bucket = storage.bucket()
    blob_name = f"bank_statements/{business_id}/{uuid4().hex}_{file.filename}"
    blob = bucket.blob(blob_name)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the maximum limit of 10MB.",
        )
    blob.upload_from_string(
        content,
        content_type=file.content_type or "application/octet-stream",
    )
    return BankStatementUploadResponse(
        file_url=blob.public_url,
        gs_url=f"gs://{bucket.name}/{blob.name}",
        content_type=file.content_type or "application/octet-stream",
        filename=file.filename or f"bank_statement_{business_id}_{uuid4().hex}.pdf",
    )


@router.get("/bank-statement", status_code=status.HTTP_200_OK)
async def get_financial_summary(business_id: str) -> list[FinancialReportInDB]:
    return await financial_service.list_financial_reports_by_business(business_id)
