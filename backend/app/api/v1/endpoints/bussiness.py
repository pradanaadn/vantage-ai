from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_user
from app.schemas.auth import UserInfo
from app.schemas.business import BusinessCreate, BusinessInDB, BusinessUpdate
from app.services import business_service

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[BusinessInDB])
async def list_businesses(
	current_user: UserInfo = Depends(get_current_user),
) -> list[BusinessInDB]:
	return await business_service.list_businesses(current_user.uid)


@router.get("/{business_id}", response_model=BusinessInDB)
async def get_business_info(
	business_id: str,
	current_user: UserInfo = Depends(get_current_user),
) -> BusinessInDB:
	try:
		business = await business_service.get_business(business_id, current_user.uid)
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
	return business


@router.post("/", response_model=BusinessInDB, status_code=status.HTTP_201_CREATED)
async def create_business(
	payload: BusinessCreate,
	current_user: UserInfo = Depends(get_current_user),
) -> BusinessInDB:
	return await business_service.create_business(payload, current_user.uid)


@router.put("/{business_id}", response_model=BusinessInDB)
async def update_business(
	business_id: str,
	payload: BusinessUpdate,
	current_user: UserInfo = Depends(get_current_user),
) -> BusinessInDB:
	try:
		business = await business_service.update_business(
			business_id,
			payload,
			current_user.uid,
		)
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
	return business


@router.delete("/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business(
	business_id: str,
	current_user: UserInfo = Depends(get_current_user),
) -> None:
	try:
		deleted = await business_service.delete_business(
			business_id,
			current_user.uid,
		)
	except PermissionError:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Forbidden",
		)
	if not deleted:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Business not found.",
		)
