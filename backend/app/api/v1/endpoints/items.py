from fastapi import APIRouter, HTTPException
from prefect.deployments import run_deployment
from app.core.config import settings

router = APIRouter()

@router.post("/audit")
async def start_invoice_audit(image_url: str):
    """
    Triggers 'The Shield' audit flow remotely via Prefect Cloud.
    This does NOT run the function locally; it sends a request to Prefect's API.
    """
    try:
        # This communicates with Prefect Cloud URL to schedule the task
        flow_run = await run_deployment(
            name=settings.PREFECT_DEPLOYMENT_NAME,
            parameters={"image_url": image_url},
            timeout=0  # 0 means fire-and-forget, returns immediately with flow run info
        )
        return {
            "message": "Audit flow scheduled in Prefect Cloud",
            "flow_run_id": str(flow_run.id),
            "state": str(flow_run.state.type)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to trigger Prefect deployment: {str(e)}"
        )

@router.get("/")
async def read_items():
    return [{"id": 1, "name": "Global Server A1"}]
