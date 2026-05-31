from loguru import logger
from prefect import flow

from app.flows.secret_task import gemini_secret
from app.models.bussines import BusinessResearchResult
from app.repositories import firestore_business
from app.schemas.business import BusinessUpdate
from app.services import business_service
from app.services.bussiness_analysis import analyze_business


@flow(name="analyze-business-flow")
async def analyze_business_flow(
    bussiness_name: str,
    bussiness_google_maps_link: str,
    bussiness_id: str,
) -> dict:
    initialize_firebase()

    try:
        gemini_api_key = gemini_secret("gemini-api-key")
    except Exception as e:
        logger.error(f"Error retrieving Gemini API key from Prefect Secret: {e}")
        raise
    
    with open("prompts/bussiness_analyst.md", "r") as f:
        system_instruction = f.read()
    analysis_result = await analyze_business(
        business_name=bussiness_name,
        business_google_maps_url=bussiness_google_maps_link,
        system_instruction=system_instruction,
        api_key=gemini_api_key,
    )
    if not isinstance(analysis_result, BusinessResearchResult):
        raise ValueError("Analysis result is not of type BusinessResearchResult")

    owner_uid = firestore_business.get_business_owner_uid(bussiness_id)
    if not owner_uid:
        logger.error(
            "Missing business owner for analysis update: %s",
            bussiness_id,
        )
        return analysis_result.model_dump()

    updated_business = BusinessUpdate.model_validate_json(
        analysis_result.model_dump_json()
    )

    await business_service.update_business(
        bussiness_id,
        updated_business,
        owner_uid,
    )
    return analysis_result.model_dump()


if __name__ == "__main__":
    from app.infra.firebase import initialize_firebase

    analyze_business_flow.serve()
