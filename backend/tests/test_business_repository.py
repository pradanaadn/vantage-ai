import pytest
from datetime import datetime, timezone

from app.repositories import firestore_business
from app.schemas.business import BusinessCreate, BusinessUpdate, CompetitorCreate, CompetitorUpdate
from app.models.bussines import Location, CompetitorType


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


@pytest.fixture
def sample_competitor(sample_location):
    return CompetitorCreate(
        business_id="",
        analysis_date=datetime.now(timezone.utc),
        name="Toko XYZ",
        industry="Retail",
        google_maps_rating=4.0,
        competitor_type=CompetitorType.DIRECT,
        google_maps_number_of_reviews=100,
        google_maps_url="https://maps.google.com/?q=Toko+XYZ",
        location=sample_location,
    )


def test_business_crud(sample_business):
    owner_uid = "user-1"
    created = firestore_business.create_business(sample_business, owner_uid)
    try:
        fetched = firestore_business.get_business(created.id, owner_uid)
        assert fetched is not None
        assert fetched.name == sample_business.name

        updated = firestore_business.update_business(
            created.id,
            BusinessUpdate(name="Toko ABC Updated"),
            owner_uid,
        )
        assert updated is not None
        assert updated.name == "Toko ABC Updated"

        all_businesses = firestore_business.list_businesses(owner_uid)
        assert any(b.id == created.id for b in all_businesses)
    finally:
        firestore_business.delete_business(created.id, owner_uid)


def test_competitor_crud(sample_business, sample_competitor):
    owner_uid = "user-1"
    created_business = firestore_business.create_business(sample_business, owner_uid)
    competitor_payload = sample_competitor.model_copy()
    competitor_payload.business_id = created_business.id

    created_competitor = firestore_business.create_competitor(
        competitor_payload,
        owner_uid,
    )
    try:
        fetched = firestore_business.get_competitor(created_competitor.id, owner_uid)
        assert fetched is not None
        assert fetched.business_id == created_business.id

        updated = firestore_business.update_competitor(
            created_competitor.id,
            CompetitorUpdate(name="Toko XYZ Updated"),
            owner_uid,
        )
        assert updated is not None
        assert updated.name == "Toko XYZ Updated"

        competitors = firestore_business.list_competitors_by_business(
            created_business.id,
            owner_uid,
        )
        assert any(c.id == created_competitor.id for c in competitors)
    finally:
        firestore_business.delete_competitor(created_competitor.id, owner_uid)
        firestore_business.delete_business(created_business.id, owner_uid)
