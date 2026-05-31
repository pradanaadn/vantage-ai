from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.financial import BankStatement
from app.schemas.file_upload import FileUpload


class BankStatementCreate(BaseModel):
    business_id: str
    statement: BankStatement


class BankStatementUpdate(BaseModel):
    statement: Optional[BankStatement] = None


class BankStatementInDB(BaseModel):
    id: str
    business_id: str
    statement: BankStatement
    owner_uid: str


class FinancialReportCreate(BaseModel):
    business_id: str
    file_url: str
    bank_statement: BankStatement | None = None
    generated_at: datetime
    created_at: datetime


class FinancialReportUpdate(BaseModel):
    file_url: Optional[str] = None
    bank_statement: Optional[BankStatement] = None
    generated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class FinancialReportInDB(FinancialReportCreate):
    id: str
    owner_uid: str


class FinancialReportCreateRequest(BaseModel):
    business_id: str
    file: FileUpload
    bank_statement: BankStatement | None = None
    generated_at: datetime | None = None
    created_at: datetime | None = None


class BankStatementUploadRequest(BaseModel):
    business_id: str
    file_url: str


class BankStatementUploadResponse(BaseModel):
    file_url: str
    gs_url: str
    content_type: str
    filename: str


class BankStatementCategorizeResponse(BaseModel):
    flow_run_id: str


