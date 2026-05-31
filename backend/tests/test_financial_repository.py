import pytest
from datetime import datetime, timezone

from app.repositories import firestore_business, firestore_financial
from app.schemas.business import BusinessCreate
from app.schemas.financial import (
    BankStatementCreate,
    BankStatementUpdate,
    FinancialReportCreate,
    FinancialReportUpdate,
)
from app.models.bussines import Location
from app.models.financial import BankStatement, Transaction, TransactionCategory, TransactionType


@pytest.fixture
def sample_location():
    return Location(
        address="Jl. Merdeka No. 1",
        subdistrict="Gambir",
        city="Jakarta Pusat",
        state="DKI Jakarta",
        country="Indonesia",
        latitude=-6.1751,
        longitude=106.8272,
    )


@pytest.fixture
def sample_business(sample_location):
    return BusinessCreate(
        name="Toko ABC",
        industry="Retail",
        google_maps_url="https://maps.google.com/?q=Toko+ABC",
        google_maps_rating=4.5,
        google_maps_number_of_reviews=150,
        location=sample_location,
        financial_report=None,
        analysis=None,
    )


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


def test_bank_statement_crud(sample_business):
    owner_uid = "user-1"
    created_business = firestore_business.create_business(sample_business, owner_uid)
    statement_payload = BankStatementCreate(
        business_id=created_business.id,
        statement=_sample_statement(),
    )

    created_statement = firestore_financial.create_bank_statement(
        statement_payload,
        owner_uid,
    )
    try:
        fetched = firestore_financial.get_bank_statement(
            created_statement.id,
            owner_uid,
        )
        assert fetched is not None
        assert fetched.business_id == created_business.id

        updated_statement = _sample_statement()
        updated_statement.final_balance = 200000.0

        updated = firestore_financial.update_bank_statement(
            created_statement.id,
            BankStatementUpdate(statement=updated_statement),
            owner_uid,
        )
        assert updated is not None
        assert updated.statement.final_balance == 200000.0

        statements = firestore_financial.list_bank_statements_by_business(
            created_business.id,
            owner_uid,
        )
        assert any(s.id == created_statement.id for s in statements)
    finally:
        firestore_financial.delete_bank_statement(created_statement.id, owner_uid)
        firestore_business.delete_business(created_business.id, owner_uid)


def test_financial_report_crud(sample_business):
    owner_uid = "user-1"
    created_business = firestore_business.create_business(sample_business, owner_uid)
    report_payload = FinancialReportCreate(
        business_id=created_business.id,
        file_url="https://storage.example.com/report.pdf",
        bank_statement=_sample_statement(),
        generated_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
    )

    created_report = firestore_financial.create_financial_report(
        report_payload,
        owner_uid,
    )
    try:
        fetched = firestore_financial.get_financial_report(
            created_report.id,
            owner_uid,
        )
        assert fetched is not None
        assert fetched.business_id == created_business.id

        updated_report = firestore_financial.update_financial_report(
            created_report.id,
            FinancialReportUpdate(
                file_url="https://storage.example.com/updated.pdf"
            ),
            owner_uid,
        )
        assert updated_report is not None
        assert updated_report.file_url.endswith("updated.pdf")

        reports = firestore_financial.list_financial_reports_by_business(
            created_business.id,
            owner_uid,
        )
        assert any(r.id == created_report.id for r in reports)
    finally:
        firestore_financial.delete_financial_report(created_report.id, owner_uid)
        firestore_business.delete_business(created_business.id, owner_uid)
