from __future__ import annotations

from typing import List, Optional

from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

from app.schemas.financial import (
    BankStatementCreate,
    BankStatementInDB,
    BankStatementUpdate,
    FinancialReportCreate,
    FinancialReportInDB,
    FinancialReportUpdate,
)

BANK_STATEMENTS_COLLECTION = "bank_statements"
FINANCIAL_REPORTS_COLLECTION = "financial_reports"


def _db():
    return firestore.client()


def create_bank_statement(statement_data: BankStatementCreate) -> BankStatementInDB:
    doc_ref = _db().collection(BANK_STATEMENTS_COLLECTION).document()
    payload = statement_data.model_dump(exclude_none=True)
    doc_ref.set(payload)
    return BankStatementInDB.model_validate({"id": doc_ref.id, **payload})


def get_bank_statement(statement_id: str) -> Optional[BankStatementInDB]:
    doc_ref = _db().collection(BANK_STATEMENTS_COLLECTION).document(statement_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None
    payload = doc.to_dict() or {} # type: ignore
    return BankStatementInDB.model_validate({"id": doc.id, **payload})


def list_bank_statements_by_business(business_id: str) -> List[BankStatementInDB]:
    docs = (
        _db()
        .collection(BANK_STATEMENTS_COLLECTION)
        .where(filter=FieldFilter("business_id", "==", business_id))
        .stream()
    )
    results: List[BankStatementInDB] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        results.append(BankStatementInDB.model_validate({"id": doc.id, **payload}))
    return results


def update_bank_statement(
    statement_id: str, statement_data: BankStatementUpdate
) -> Optional[BankStatementInDB]:
    doc_ref = _db().collection(BANK_STATEMENTS_COLLECTION).document(statement_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None

    update_payload = statement_data.model_dump(exclude_none=True)
    if update_payload:
        doc_ref.update(update_payload)

    updated = doc_ref.get()
    payload = updated.to_dict() or {} # pyright: ignore[reportAttributeAccessIssue]
    return BankStatementInDB.model_validate({"id": updated.id, **payload})


def delete_bank_statement(statement_id: str) -> bool:
    doc_ref = _db().collection(BANK_STATEMENTS_COLLECTION).document(statement_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return False
    doc_ref.delete()
    return True


def create_financial_report(report_data: FinancialReportCreate) -> FinancialReportInDB:
    doc_ref = _db().collection(FINANCIAL_REPORTS_COLLECTION).document()
    payload = report_data.model_dump(exclude_none=True)
    doc_ref.set(payload)
    return FinancialReportInDB.model_validate({"id": doc_ref.id, **payload})


def get_financial_report(report_id: str) -> Optional[FinancialReportInDB]:
    doc_ref = _db().collection(FINANCIAL_REPORTS_COLLECTION).document(report_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None
    payload = doc.to_dict() or {} # type: ignore
    return FinancialReportInDB.model_validate({"id": doc.id, **payload})


def list_financial_reports_by_business(business_id: str) -> List[FinancialReportInDB]:
    docs = (
        _db()
        .collection(FINANCIAL_REPORTS_COLLECTION)
        .where(filter=FieldFilter("business_id", "==", business_id))
        .stream()
    )
    results: List[FinancialReportInDB] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        results.append(FinancialReportInDB.model_validate({"id": doc.id, **payload}))
    return results


def update_financial_report(
    report_id: str, report_data: FinancialReportUpdate
) -> Optional[FinancialReportInDB]:
    doc_ref = _db().collection(FINANCIAL_REPORTS_COLLECTION).document(report_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None

    update_payload = report_data.model_dump(exclude_none=True)
    if update_payload:
        doc_ref.update(update_payload)

    updated = doc_ref.get()
    payload = updated.to_dict() or {} # pyright: ignore[reportAttributeAccessIssue]
    return FinancialReportInDB.model_validate({"id": updated.id, **payload})


def delete_financial_report(report_id: str) -> bool:
    doc_ref = _db().collection(FINANCIAL_REPORTS_COLLECTION).document(report_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return False
    doc_ref.delete()
    return True
