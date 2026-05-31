from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_user
from app.schemas.auth import UserInfo
from app.schemas.business import (
	BusinessCreate,
	BusinessAnalyzeRequest,
	BusinessAnalyzeResponse,
	BusinessInDB,
	BusinessUpdate,
	CompetitorInDB,
)
from prefect.deployments import arun_deployment
from app.services import business_service

router = APIRouter(dependencies=[Depends(get_current_user)])


async def _ensure_business_owner(
	business_id: str,
	owner_uid: str,
) -> None:
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


@router.get("/", response_model=list[BusinessInDB])
async def list_businesses(
	current_user: UserInfo = Depends(get_current_user),
) -> list[BusinessInDB]:
	return await business_service.list_businesses(current_user.uid)

@router.post("/analyze", response_model=BusinessAnalyzeResponse, status_code=status.HTTP_201_CREATED)
async def analyze_business(
	payload: BusinessAnalyzeRequest,
	current_user: UserInfo = Depends(get_current_user),
) -> BusinessAnalyzeResponse:
	try:
		business = await business_service.get_business(
			payload.business_id,
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
	flow_run = await arun_deployment(
		"analyze-business-flow/analyze-business-flow",
		parameters={
			"bussiness_name": business.name,
			"bussiness_google_maps_link": business.google_maps_url,
			"bussiness_id": payload.business_id,
		},
		timeout=0,
	)
	if not flow_run:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Failed to start business analysis flow.",
		)
	if not flow_run.id:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Flow run did not return a valid ID.",
		)
	return BusinessAnalyzeResponse(flow_run_id=str(flow_run.id))
        
@router.get("/{business_id}/competitors", response_model=list[CompetitorInDB])
async def list_competitors(
	business_id: str,
	current_user: UserInfo = Depends(get_current_user),
) -> list[CompetitorInDB]:
	await _ensure_business_owner(business_id, current_user.uid)
	return await business_service.list_competitors_by_business(
		business_id,
		current_user.uid,
	)


@router.get("/competitors/{competitor_id}", response_model=CompetitorInDB)
async def get_competitor(
	competitor_id: str,
	current_user: UserInfo = Depends(get_current_user),
) -> CompetitorInDB:
	try:
		competitor = await business_service.get_competitor(
			competitor_id,
			current_user.uid,
		)
	except PermissionError:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Forbidden",
		)
	if not competitor:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Competitor not found.",
		)
	return competitor


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
