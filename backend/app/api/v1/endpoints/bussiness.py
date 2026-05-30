from fastapi import APIRouter, HTTPException, status
from app.schemas.business import BusinessCreate, BusinessInDB, BusinessUpdate
from app.services import business_service

router = APIRouter()


@router.get("/", response_model=list[BusinessInDB])
async def list_businesses() -> list[BusinessInDB]:
	return await business_service.list_businesses()


@router.get("/{business_id}", response_model=BusinessInDB)
async def get_business_info(business_id: str) -> BusinessInDB:
	business = await business_service.get_business(business_id)
	if not business:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Business not found.",
		)
	return business


@router.post("/", response_model=BusinessInDB, status_code=status.HTTP_201_CREATED)
async def create_business(payload: BusinessCreate) -> BusinessInDB:
	return await business_service.create_business(payload)


@router.put("/{business_id}", response_model=BusinessInDB)
async def update_business(
	business_id: str,
	payload: BusinessUpdate,
) -> BusinessInDB:
	business = await business_service.update_business(business_id, payload)
	if not business:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Business not found.",
		)
	return business


@router.delete("/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business(business_id: str) -> None:
	deleted = await business_service.delete_business(business_id)
	if not deleted:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Business not found.",
		)
