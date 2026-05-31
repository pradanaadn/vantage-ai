from __future__ import annotations

from typing import List
from loguru import logger
from google.api_core.exceptions import GoogleAPIError

from app.repositories import firestore_business
from app.schemas.business import (
    BusinessCreate,
    BusinessInDB,
    BusinessUpdate,
    CompetitorCreate,
    CompetitorInDB,
    CompetitorUpdate,
)


async def create_business(business_data: BusinessCreate, owner_uid: str) -> BusinessInDB:
    try:
        logger.info("Creating business")
        return firestore_business.create_business(business_data, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while creating business: {e}")
        raise


async def get_business(business_id: str, owner_uid: str) -> BusinessInDB | None:
    try:
        logger.info(f"Fetching business {business_id}")
        return firestore_business.get_business(business_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while fetching business {business_id}: {e}")
        raise


async def list_businesses(owner_uid: str) -> List[BusinessInDB]:
    try:
        logger.info("Listing businesses")
        return firestore_business.list_businesses(owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while listing businesses: {e}")
        raise


async def update_business(
    business_id: str,
    business_data: BusinessUpdate,
    owner_uid: str,
) -> BusinessInDB | None:
    try:
        logger.info(f"Updating business {business_id}")
        return firestore_business.update_business(
            business_id,
            business_data,
            owner_uid,
        )
    except GoogleAPIError as e:
        logger.error(f"Firestore error while updating business {business_id}: {e}")
        raise


async def delete_business(business_id: str, owner_uid: str) -> bool:
    try:
        logger.info(f"Deleting business {business_id}")
        return firestore_business.delete_business(business_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while deleting business {business_id}: {e}")
        raise


async def create_competitor(
    competitor_data: CompetitorCreate,
    owner_uid: str,
) -> CompetitorInDB:
    try:
        logger.info("Creating competitor")
        return firestore_business.create_competitor(competitor_data, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while creating competitor: {e}")
        raise


async def get_competitor(
    competitor_id: str,
    owner_uid: str,
) -> CompetitorInDB | None:
    try:
        logger.info(f"Fetching competitor {competitor_id}")
        return firestore_business.get_competitor(competitor_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while fetching competitor {competitor_id}: {e}")
        raise


async def list_competitors_by_business(
    business_id: str,
    owner_uid: str,
) -> List[CompetitorInDB]:
    try:
        logger.info(f"Listing competitors for business {business_id}")
        return firestore_business.list_competitors_by_business(business_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(
            f"Firestore error while listing competitors for business {business_id}: {e}"
        )
        raise


async def update_competitor(
    competitor_id: str,
    competitor_data: CompetitorUpdate,
    owner_uid: str,
) -> CompetitorInDB | None:
    try:
        logger.info(f"Updating competitor {competitor_id}")
        return firestore_business.update_competitor(
            competitor_id,
            competitor_data,
            owner_uid,
        )
    except GoogleAPIError as e:
        logger.error(f"Firestore error while updating competitor {competitor_id}: {e}")
        raise


async def delete_competitor(competitor_id: str, owner_uid: str) -> bool:
    try:
        logger.info(f"Deleting competitor {competitor_id}")
        return firestore_business.delete_competitor(competitor_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while deleting competitor {competitor_id}: {e}")
        raise
