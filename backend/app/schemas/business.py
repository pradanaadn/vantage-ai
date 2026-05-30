from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.bussines import Location, BussinessAnalysis, CompetitorType
from app.models.financial import FinancialReport


class BusinessBase(BaseModel):
    name: str = Field(..., description="Nama bisnis")
    industry: str = Field(..., description="Industri bisnis")
    google_maps_url: str = Field(..., description="URL Google Maps bisnis")
    google_maps_rating: Optional[float] = Field(
        None, description="Rating bisnis di Google Maps"
    )
    google_maps_number_of_reviews: Optional[int] = Field(
        None, description="Jumlah ulasan bisnis di Google Maps"
    )
    location: Optional[Location] = Field(None, description="Lokasi bisnis")
    financial_report: Optional[List[FinancialReport]] = Field(
        None, description="Laporan keuangan bisnis"
    )
    analysis: Optional[List[BussinessAnalysis]] = Field(
        None, description="Analisis bisnis"
    )


class BusinessCreate(BaseModel):
    name: str = Field(..., description="Nama bisnis")
    industry: str = Field(..., description="Industri bisnis")
    google_maps_url: str = Field(..., description="URL Google Maps bisnis")


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    google_maps_url: Optional[str] = None
    google_maps_rating: Optional[float] = None
    google_maps_number_of_reviews: Optional[int] = None
    location: Optional[Location] = None
    financial_report: Optional[List[FinancialReport]] = None
    analysis: Optional[List[BussinessAnalysis]] = None


class BusinessInDB(BusinessBase):
    id: str


class CompetitorBase(BaseModel):
    analysis_date: datetime = Field(..., description="Tanggal analisis dilakukan")
    name: str = Field(..., description="Nama kompetitor")
    industry: str = Field(..., description="Industri kompetitor")
    google_maps_rating: float = Field(
        ..., description="Rating kompetitor di Google Maps"
    )
    competitor_type: CompetitorType = Field(..., description="Tipe kompetitor")
    competitor_analysis: Optional[List[BussinessAnalysis]] = Field(
        None, description="Analisis kompetitor"
    )
    google_maps_number_of_reviews: int = Field(
        ..., description="Jumlah ulasan kompetitor di Google Maps"
    )
    google_maps_url: str = Field(..., description="URL Google Maps kompetitor")
    location: Location = Field(..., description="Lokasi kompetitor")


class CompetitorCreate(CompetitorBase):
    business_id: str


class CompetitorUpdate(BaseModel):
    analysis_date: Optional[datetime] = None
    name: Optional[str] = None
    industry: Optional[str] = None
    google_maps_rating: Optional[float] = None
    competitor_type: Optional[CompetitorType] = None
    competitor_analysis: Optional[List[BussinessAnalysis]] = None
    google_maps_number_of_reviews: Optional[int] = None
    google_maps_url: Optional[str] = None
    location: Optional[Location] = None


class CompetitorInDB(CompetitorBase):
    id: str
    business_id: str
