from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from app.api.deps import get_current_user
from app.schemas.auth import UserInfo
from app.schemas.financial import (
    BankStatementCategorizeResponse,
    BankStatementUploadRequest,
    BankStatementUploadResponse,
    FinancialReportInDB,
)
from app.services import business_service
from app.services import financial_service
from firebase_admin import storage
from uuid import uuid4
from prefect.deployments import arun_deployment
from app.core.config import settings

router = APIRouter(dependencies=[Depends(get_current_user)])


async def _ensure_business_owner(business_id: str, owner_uid: str) -> None:
    try:
        business = await business_service.get_business(business_id, owner_uid)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found.",
        )


@router.post("/bank-statement/extract", status_code=status.HTTP_201_CREATED)
async def extract_and_categorize_bank_statement(
    payload: BankStatementUploadRequest,
    current_user: UserInfo = Depends(get_current_user),
) -> BankStatementCategorizeResponse:
    await _ensure_business_owner(payload.business_id, current_user.uid)
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


@router.post("/bank-statement/test", status_code=status.HTTP_201_CREATED)
async def test(
    payload: BankStatementUploadRequest,
    current_user: UserInfo = Depends(get_current_user),
) -> BankStatementCategorizeResponse:
    await _ensure_business_owner(payload.business_id, current_user.uid)
    flow_run = await arun_deployment(
        "test-categorize-bank-statement/test-categorize-bank-statement",
        parameters={
            "bussiness_id": payload.business_id,
        },
        timeout=0
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
    current_user: UserInfo = Depends(get_current_user),
) -> BankStatementUploadResponse:
    await _ensure_business_owner(business_id, current_user.uid)
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only PDF files are allowed.",
        )

    bucket = storage.bucket()
    blob_name = f"bank_statements/{business_id}/{uuid4().hex}_{file.filename}"
    blob = bucket.blob(blob_name)
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        max_mb = settings.MAX_FILE_SIZE // (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the maximum limit of {max_mb}MB.",
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
async def get_financial_summary(
    business_id: str,
    current_user: UserInfo = Depends(get_current_user),
) -> list[FinancialReportInDB]:
    await _ensure_business_owner(business_id, current_user.uid)
    return await financial_service.list_financial_reports_by_business(
        business_id,
        current_user.uid,
    )
