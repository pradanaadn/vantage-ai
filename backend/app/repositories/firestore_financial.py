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


def create_bank_statement(
    statement_data: BankStatementCreate,
    owner_uid: str,
) -> BankStatementInDB:
    doc_ref = _db().collection(BANK_STATEMENTS_COLLECTION).document()
    payload = statement_data.model_dump(exclude_none=True)
    payload["owner_uid"] = owner_uid
    doc_ref.set(payload)
    return BankStatementInDB.model_validate({"id": doc_ref.id, **payload})


def get_bank_statement(
    statement_id: str,
    owner_uid: str,
) -> Optional[BankStatementInDB]:
    doc_ref = _db().collection(BANK_STATEMENTS_COLLECTION).document(statement_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None
    payload = doc.to_dict() or {} # type: ignore
    if payload.get("owner_uid") != owner_uid:
        raise PermissionError("Bank statement does not belong to the user")
    return BankStatementInDB.model_validate({"id": doc.id, **payload})


def list_bank_statements_by_business(
    business_id: str,
    owner_uid: str,
) -> List[BankStatementInDB]:
    docs = (
        _db()
        .collection(BANK_STATEMENTS_COLLECTION)
        .where(filter=FieldFilter("business_id", "==", business_id))
        .where(filter=FieldFilter("owner_uid", "==", owner_uid))
        .stream()
    )
    results: List[BankStatementInDB] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        results.append(BankStatementInDB.model_validate({"id": doc.id, **payload}))
    return results


def update_bank_statement(
    statement_id: str,
    statement_data: BankStatementUpdate,
    owner_uid: str,
) -> Optional[BankStatementInDB]:
    doc_ref = _db().collection(BANK_STATEMENTS_COLLECTION).document(statement_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None
    payload = doc.to_dict() or {} # type: ignore
    if payload.get("owner_uid") != owner_uid:
        raise PermissionError("Bank statement does not belong to the user")

    update_payload = statement_data.model_dump(exclude_none=True)
    if update_payload:
        doc_ref.update(update_payload)

    updated = doc_ref.get()
    payload = updated.to_dict() or {} # pyright: ignore[reportAttributeAccessIssue]
    return BankStatementInDB.model_validate({"id": updated.id, **payload})


def delete_bank_statement(statement_id: str, owner_uid: str) -> bool:
    doc_ref = _db().collection(BANK_STATEMENTS_COLLECTION).document(statement_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return False
    payload = doc.to_dict() or {} # type: ignore
    if payload.get("owner_uid") != owner_uid:
        raise PermissionError("Bank statement does not belong to the user")
    doc_ref.delete()
    return True


def create_financial_report(
    report_data: FinancialReportCreate,
    owner_uid: str,
) -> FinancialReportInDB:
    doc_ref = _db().collection(FINANCIAL_REPORTS_COLLECTION).document()
    payload = report_data.model_dump(exclude_none=True)
    payload["owner_uid"] = owner_uid
    doc_ref.set(payload)
    return FinancialReportInDB.model_validate({"id": doc_ref.id, **payload})


def get_financial_report(
    report_id: str,
    owner_uid: str,
) -> Optional[FinancialReportInDB]:
    doc_ref = _db().collection(FINANCIAL_REPORTS_COLLECTION).document(report_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None
    payload = doc.to_dict() or {} # type: ignore
    if payload.get("owner_uid") != owner_uid:
        raise PermissionError("Financial report does not belong to the user")
    return FinancialReportInDB.model_validate({"id": doc.id, **payload})


def list_financial_reports_by_business(
    business_id: str,
    owner_uid: str,
) -> List[FinancialReportInDB]:
    docs = (
        _db()
        .collection(FINANCIAL_REPORTS_COLLECTION)
        .where(filter=FieldFilter("business_id", "==", business_id))
        .where(filter=FieldFilter("owner_uid", "==", owner_uid))
        .stream()
    )
    results: List[FinancialReportInDB] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        results.append(FinancialReportInDB.model_validate({"id": doc.id, **payload}))
    return results


def update_financial_report(
    report_id: str,
    report_data: FinancialReportUpdate,
    owner_uid: str,
) -> Optional[FinancialReportInDB]:
    doc_ref = _db().collection(FINANCIAL_REPORTS_COLLECTION).document(report_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None
    payload = doc.to_dict() or {} # pyright: ignore[reportAttributeAccessIssue]
    if payload.get("owner_uid") != owner_uid:
        raise PermissionError("Financial report does not belong to the user")

    update_payload = report_data.model_dump(exclude_none=True)
    if update_payload:
        doc_ref.update(update_payload)

    updated = doc_ref.get()
    payload = updated.to_dict() or {} # pyright: ignore[reportAttributeAccessIssue]
    return FinancialReportInDB.model_validate({"id": updated.id, **payload})


def delete_financial_report(report_id: str, owner_uid: str) -> bool:
    doc_ref = _db().collection(FINANCIAL_REPORTS_COLLECTION).document(report_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return False
    payload = doc.to_dict() or {} # pyright: ignore[reportAttributeAccessIssue]
    if payload.get("owner_uid") != owner_uid:
        raise PermissionError("Financial report does not belong to the user")
    doc_ref.delete()
    return True
