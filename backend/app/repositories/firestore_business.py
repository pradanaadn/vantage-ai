from __future__ import annotations

from typing import List, Optional

from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

from app.schemas.business import (
    BusinessCreate,
    BusinessInDB,
    BusinessUpdate,
    CompetitorCreate,
    CompetitorInDB,
    CompetitorUpdate,
)

BUSINESSES_COLLECTION = "businesses"
COMPETITORS_COLLECTION = "competitors"


def _db():
    return firestore.client()


def create_business(business_data: BusinessCreate) -> BusinessInDB:
    doc_ref = _db().collection(BUSINESSES_COLLECTION).document()
    payload = business_data.model_dump(exclude_none=True)
    doc_ref.set(payload)
    return BusinessInDB.model_validate({"id": doc_ref.id, **payload})


def get_business(business_id: str) -> Optional[BusinessInDB]:
    doc_ref = _db().collection(BUSINESSES_COLLECTION).document(business_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None
    payload = doc.to_dict() or {} # type: ignore
    return BusinessInDB.model_validate({"id": doc.id, **payload}) # type: ignore


def list_businesses() -> List[BusinessInDB]:
    docs = _db().collection(BUSINESSES_COLLECTION).stream()
    results: List[BusinessInDB] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        results.append(BusinessInDB.model_validate({"id": doc.id, **payload}))
    return results


def update_business(business_id: str, business_data: BusinessUpdate) -> Optional[BusinessInDB]:
    doc_ref = _db().collection(BUSINESSES_COLLECTION).document(business_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None

    update_payload = business_data.model_dump(exclude_none=True)
    if update_payload:
        doc_ref.update(update_payload)

    updated = doc_ref.get()
    payload = updated.to_dict() or {} # pyright: ignore[reportAttributeAccessIssue]
    return BusinessInDB.model_validate({"id": updated.id, **payload}) # type: ignore


def delete_business(business_id: str) -> bool:
    doc_ref = _db().collection(BUSINESSES_COLLECTION).document(business_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return False
    doc_ref.delete()
    return True


def create_competitor(competitor_data: CompetitorCreate) -> CompetitorInDB:
    doc_ref = _db().collection(COMPETITORS_COLLECTION).document()
    payload = competitor_data.model_dump(exclude_none=True)
    doc_ref.set(payload)
    return CompetitorInDB.model_validate({"id": doc_ref.id, **payload})


def get_competitor(competitor_id: str) -> Optional[CompetitorInDB]:
    doc_ref = _db().collection(COMPETITORS_COLLECTION).document(competitor_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None
    payload = doc.to_dict() or {} # type: ignore
    return CompetitorInDB.model_validate({"id": doc.id, **payload}) # pyright: ignore[reportAttributeAccessIssue]


def list_competitors_by_business(business_id: str) -> List[CompetitorInDB]:
    docs = (
        _db()
        .collection(COMPETITORS_COLLECTION)
        .where(filter=FieldFilter("business_id", "==", business_id))
        .stream()
    )
    results: List[CompetitorInDB] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        results.append(CompetitorInDB.model_validate({"id": doc.id, **payload}))
    return results


def update_competitor(
    competitor_id: str, competitor_data: CompetitorUpdate
) -> Optional[CompetitorInDB]:
    doc_ref = _db().collection(COMPETITORS_COLLECTION).document(competitor_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return None

    update_payload = competitor_data.model_dump(exclude_none=True)
    if update_payload:
        doc_ref.update(update_payload)

    updated = doc_ref.get()
    payload = updated.to_dict() or {} # pyright: ignore[reportAttributeAccessIssue]
    return CompetitorInDB.model_validate({"id": updated.id, **payload}) # type: ignore


def delete_competitor(competitor_id: str) -> bool:
    doc_ref = _db().collection(COMPETITORS_COLLECTION).document(competitor_id)
    doc = doc_ref.get()
    if not doc.exists: # pyright: ignore[reportAttributeAccessIssue]
        return False
    doc_ref.delete()
    return True
