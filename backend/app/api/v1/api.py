from fastapi import APIRouter
from app.api.v1.endpoints import auth, bussiness, financial

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(bussiness.router, prefix="/business", tags=["business"])
api_router.include_router(financial.router, prefix="/financial", tags=["financial"])
