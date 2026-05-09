from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vantage AI"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # Prefect Cloud Configuration
    PREFECT_API_URL: str | None = None
    PREFECT_API_KEY: str | None = None
    PREFECT_DEPLOYMENT_NAME: str = "invoice-audit-flow/vantage-prod"

    class Config:
        case_sensitive = True

settings = Settings()
