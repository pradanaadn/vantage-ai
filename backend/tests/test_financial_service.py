import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from app.models.financial import BankStatement, Transaction, TransactionCategory, TransactionType
from app.schemas.financial import (
    BankStatementCreate,
    BankStatementInDB,
    FinancialReportCreateRequest,
    FinancialReportInDB,
)
from app.schemas.file_upload import FileUpload
from app.services import financial_service


def _sample_statement():
    transaction = Transaction(
        date=datetime.now(timezone.utc),
        description="Pembayaran",
        type=TransactionType.CREDIT,
        category=TransactionCategory.PENDAPATAN_OPERASIONAL,
        subcategory=None,
        amount=100000.0,
        balance=150000.0,
        reference="INV-1",
    )
    return BankStatement(
        name="Toko ABC",
        account_number="1234567890",
        period_start=datetime.now(timezone.utc),
        period_end=datetime.now(timezone.utc),
        currency="IDR",
        initial_balance=50000.0,
        final_balance=150000.0,
        transactions=[transaction],
    )


@pytest.mark.asyncio
async def test_create_bank_statement_service():
    owner_uid = "user-1"
    payload = BankStatementCreate(
        business_id="biz-1",
        statement=_sample_statement(),
    )
    with patch("app.repositories.firestore_financial.create_bank_statement") as mock_create:
        mock_create.return_value = BankStatementInDB(
            id="stmt-1",
            owner_uid=owner_uid,
            **payload.model_dump(),
        )
        created = await financial_service.create_bank_statement(payload, owner_uid)
        assert created.id == "stmt-1"
        assert created.business_id == "biz-1"


@pytest.mark.asyncio
async def test_create_financial_report_service():
    owner_uid = "user-1"
    payload = FinancialReportCreateRequest(
        business_id="biz-1",
        file=FileUpload(
            filename="report.pdf",
            content_type="application/pdf",
            data=b"pdf-bytes",
        ),
        bank_statement=_sample_statement(),
    )

    mock_blob = MagicMock()
    mock_blob.public_url = "https://storage.example.com/report.pdf"

    with patch("firebase_admin.storage.bucket") as mock_bucket, \
         patch("app.repositories.firestore_financial.create_financial_report") as mock_create:
        mock_bucket.return_value.blob.return_value = mock_blob
        mock_create.return_value = FinancialReportInDB(
            id="rep-1",
            owner_uid=owner_uid,
            business_id="biz-1",
            file_url=mock_blob.public_url,
            bank_statement=payload.bank_statement,
            generated_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
        )

        created = await financial_service.create_financial_report(payload, owner_uid)
        assert created.id == "rep-1"
        assert created.file_url == mock_blob.public_url
