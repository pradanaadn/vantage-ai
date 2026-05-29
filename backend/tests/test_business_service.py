import pytest
from datetime import datetime, timezone
from unittest.mock import patch

from app.models.bussines import CompetitorType, Location
from app.schemas.business import BusinessCreate, CompetitorCreate, BusinessInDB, CompetitorInDB
from app.services import business_service


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


@pytest.mark.asyncio
async def test_create_business_service(sample_location):
    payload = BusinessCreate(
        name="Toko ABC",
        industry="Retail",
        google_maps_url="https://maps.google.com/?q=Toko+ABC",
        google_maps_rating=4.5,
        google_maps_number_of_reviews=150,
        location=sample_location,
        analysis=None,
        financial_report=None,
    )
    with patch("app.repositories.firestore_business.create_business") as mock_create:
        mock_create.return_value = BusinessInDB(id="biz-1", **payload.model_dump())
        created = await business_service.create_business(payload)
        assert created.id == "biz-1"
        assert created.name == payload.name


@pytest.mark.asyncio
async def test_create_competitor_service(sample_location):
    payload = CompetitorCreate(
        business_id="biz-1",
        analysis_date=datetime.now(timezone.utc),
        name="Toko XYZ",
        industry="Retail",
        google_maps_rating=4.0,
        competitor_type=CompetitorType.DIRECT,
        google_maps_number_of_reviews=100,
        google_maps_url="https://maps.google.com/?q=Toko+XYZ",
        location=sample_location,
    )
    with patch("app.repositories.firestore_business.create_competitor") as mock_create:
        mock_create.return_value = CompetitorInDB(id="comp-1", **payload.model_dump())
        created = await business_service.create_competitor(payload)
        assert created.id == "comp-1"
        assert created.business_id == "biz-1"
