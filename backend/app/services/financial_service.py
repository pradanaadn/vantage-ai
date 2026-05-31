from __future__ import annotations

from typing import List
from datetime import datetime, timezone
from uuid import uuid4

from firebase_admin import storage
from loguru import logger
from google.api_core.exceptions import GoogleAPIError

from app.repositories import firestore_financial
from app.schemas.financial import (
    BankStatementCreate,
    BankStatementInDB,
    BankStatementUpdate,
    FinancialAnalysisCreate,
    FinancialAnalysisInDB,
    FinancialAnalysisUpdate,
    FinancialReportCreate,
    FinancialReportCreateRequest,
    FinancialReportInDB,
    FinancialReportUpdate,
)


async def create_bank_statement(
    statement_data: BankStatementCreate,
    owner_uid: str,
) -> BankStatementInDB:
    try:
        logger.info("Creating bank statement")
        return firestore_financial.create_bank_statement(statement_data, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while creating bank statement: {e}")
        raise


async def get_bank_statement(
    statement_id: str,
    owner_uid: str,
) -> BankStatementInDB | None:
    try:
        logger.info(f"Fetching bank statement {statement_id}")
        return firestore_financial.get_bank_statement(statement_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while fetching bank statement {statement_id}: {e}")
        raise


async def list_bank_statements_by_business(
    business_id: str,
    owner_uid: str,
) -> List[BankStatementInDB]:
    try:
        logger.info(f"Listing bank statements for business {business_id}")
        return firestore_financial.list_bank_statements_by_business(
            business_id,
            owner_uid,
        )
    except GoogleAPIError as e:
        logger.error(
            f"Firestore error while listing bank statements for business {business_id}: {e}"
        )
        raise


async def update_bank_statement(
    statement_id: str,
    statement_data: BankStatementUpdate,
    owner_uid: str,
) -> BankStatementInDB | None:
    try:
        logger.info(f"Updating bank statement {statement_id}")
        return firestore_financial.update_bank_statement(
            statement_id,
            statement_data,
            owner_uid,
        )
    except GoogleAPIError as e:
        logger.error(f"Firestore error while updating bank statement {statement_id}: {e}")
        raise


async def delete_bank_statement(statement_id: str, owner_uid: str) -> bool:
    try:
        logger.info(f"Deleting bank statement {statement_id}")
        return firestore_financial.delete_bank_statement(statement_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while deleting bank statement {statement_id}: {e}")
        raise


async def create_financial_report(
    request: FinancialReportCreateRequest,
    owner_uid: str,
) -> FinancialReportInDB:
    try:
        logger.info("Uploading financial report file")
        bucket = storage.bucket()
        blob_name = (
            f"financial_reports/{request.business_id}/"
            f"{uuid4().hex}_{request.file.filename}"
        )
        blob = bucket.blob(blob_name)
        blob.upload_from_string(request.file.data, content_type=request.file.content_type)

        now = datetime.now(timezone.utc)
        report_payload = FinancialReportCreate(
            business_id=request.business_id,
            file_url=blob.public_url,
            bank_statement=request.bank_statement,
            generated_at=request.generated_at or now,
            created_at=request.created_at or now,
        )
        return firestore_financial.create_financial_report(report_payload, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while creating financial report: {e}")
        raise


async def get_financial_report(
    report_id: str,
    owner_uid: str,
) -> FinancialReportInDB | None:
    try:
        logger.info(f"Fetching financial report {report_id}")
        return firestore_financial.get_financial_report(report_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while fetching financial report {report_id}: {e}")
        raise


async def list_financial_reports_by_business(
    business_id: str,
    owner_uid: str,
) -> List[FinancialReportInDB]:
    try:
        logger.info(f"Listing financial reports for business {business_id}")
        return firestore_financial.list_financial_reports_by_business(
            business_id,
            owner_uid,
        )
    except GoogleAPIError as e:
        logger.error(
            f"Firestore error while listing financial reports for business {business_id}: {e}"
        )
        raise


async def update_financial_report(
    report_id: str,
    report_data: FinancialReportUpdate,
    owner_uid: str,
) -> FinancialReportInDB | None:
    try:
        logger.info(f"Updating financial report {report_id}")
        return firestore_financial.update_financial_report(
            report_id,
            report_data,
            owner_uid,
        )
    except GoogleAPIError as e:
        logger.error(f"Firestore error while updating financial report {report_id}: {e}")
        raise


async def delete_financial_report(report_id: str, owner_uid: str) -> bool:
    try:
        logger.info(f"Deleting financial report {report_id}")
        return firestore_financial.delete_financial_report(report_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while deleting financial report {report_id}: {e}")
        raise


async def create_financial_analysis(
    analysis_data: FinancialAnalysisCreate,
    owner_uid: str,
) -> FinancialAnalysisInDB:
    try:
        logger.info("Creating financial analysis")
        return firestore_financial.create_financial_analysis(analysis_data, owner_uid)
    except GoogleAPIError as e:
        logger.error(f"Firestore error while creating financial analysis: {e}")
        raise


async def get_financial_analysis(
    analysis_id: str,
    owner_uid: str,
) -> FinancialAnalysisInDB | None:
    try:
        logger.info(f"Fetching financial analysis {analysis_id}")
        return firestore_financial.get_financial_analysis(analysis_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(
            f"Firestore error while fetching financial analysis {analysis_id}: {e}"
        )
        raise


async def list_financial_analysis_by_business(
    business_id: str,
    owner_uid: str,
) -> List[FinancialAnalysisInDB]:
    try:
        logger.info(f"Listing financial analysis for business {business_id}")
        return firestore_financial.list_financial_analysis_by_business(
            business_id,
            owner_uid,
        )
    except GoogleAPIError as e:
        logger.error(
            f"Firestore error while listing financial analysis for business {business_id}: {e}"
        )
        raise


async def update_financial_analysis(
    analysis_id: str,
    analysis_data: FinancialAnalysisUpdate,
    owner_uid: str,
) -> FinancialAnalysisInDB | None:
    try:
        logger.info(f"Updating financial analysis {analysis_id}")
        return firestore_financial.update_financial_analysis(
            analysis_id,
            analysis_data,
            owner_uid,
        )
    except GoogleAPIError as e:
        logger.error(
            f"Firestore error while updating financial analysis {analysis_id}: {e}"
        )
        raise


async def delete_financial_analysis(analysis_id: str, owner_uid: str) -> bool:
    try:
        logger.info(f"Deleting financial analysis {analysis_id}")
        return firestore_financial.delete_financial_analysis(analysis_id, owner_uid)
    except GoogleAPIError as e:
        logger.error(
            f"Firestore error while deleting financial analysis {analysis_id}: {e}"
        )
        raise
