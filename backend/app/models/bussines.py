from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum
from .financial import FinancialReport


class CompetitorType(str, Enum):
    DIRECT = "Direct"
    INDIRECT = "Indirect"
    REPLACEMENT = "Replacement"


class BussinessAnalysis(BaseModel):
    analysis_date: datetime = Field(..., description="Tanggal analisis dilakukan")
    sentiment: str = Field(..., description="Sentimen umum tentang bisnis")
    top_positive_reviews: list[str] = Field(
        ..., description="Daftar ulasan positif utama"
    )
    top_negative_reviews: list[str] = Field(
        ..., description="Daftar ulasan negatif utama"
    )
    strengths: list[str] = Field(..., description="Kekuatan utama bisnis")
    weaknesses: list[str] = Field(..., description="Kelemahan utama bisnis")
    opportunities: list[str] = Field(
        ..., description="Peluang yang dapat dimanfaatkan oleh bisnis"
    )

    threats: list[str] = Field(..., description="Ancaman yang dihadapi oleh bisnis")


class Location(BaseModel):
    address: str = Field(..., description="Alamat lengkap lokasi")
    subdistrict: str = Field(..., description="Kecamatan lokasi")
    city: str = Field(..., description="Kota/Kabupaten lokasi")
    state: str = Field(..., description="Provinsi lokasi")
    country: str = Field(..., description="Negara lokasi")
    latitude: float = Field(..., description="Latitude lokasi")
    longitude: float = Field(..., description="Longitude lokasi")


class Business(BaseModel):
    name: str = Field(..., description="Nama bisnis")
    industry: str = Field(..., description="Industri bisnis")
    google_maps_url: str = Field(..., description="URL Google Maps bisnis")
    google_maps_rating: float = Field(..., description="Rating bisnis di Google Maps")
    google_maps_number_of_reviews: int = Field(
        ..., description="Jumlah ulasan bisnis di Google Maps"
    )
    location: Location = Field(..., description="Lokasi bisnis")
    financial_report: List[FinancialReport] | None = Field(
        None, description="Laporan keuangan bisnis"
    )
    analysis: list[BussinessAnalysis] | None = Field(
        None, description="Analisis bisnis"
    )


class BusinessResearchResult(BaseModel):
    name: str = Field(..., description="Nama bisnis")
    industry: str = Field(..., description="Industri bisnis")
    google_maps_url: str = Field(..., description="URL Google Maps bisnis")
    google_maps_rating: float = Field(..., description="Rating bisnis di Google Maps")
    google_maps_number_of_reviews: int = Field(
        ..., description="Jumlah ulasan bisnis di Google Maps"
    )
    location: Location = Field(..., description="Lokasi bisnis")
    analysis: list[BussinessAnalysis] = Field(description="Analisis bisnis")
    analysis_date: datetime = Field(..., description="Tanggal analisis dilakukan")


class Competitor(BusinessResearchResult):
    competitor_type: CompetitorType = Field(..., description="Tipe kompetitor")


class BussinessCompetitor(BaseModel):
    competitors: list[Competitor] = Field(..., description="Daftar kompetitor bisnis")

if __name__ == "__main__":
    # # Example usage
    # business = Business(
    #     name="Toko ABC",
    #     industry="Retail",
    #     google_maps_url="https://maps.google.com/?q=Toko+ABC",
    #     google_maps_rating=4.5,
    #     google_maps_number_of_reviews=150,
    #     location=Location(
    #         address="Jl. Merdeka No. 123, Jakarta",
    #         subdistrict="Gambir",
    #         city="Jakarta Pusat",
    #         state="DKI Jakarta",
    #         country="Indonesia",
    #         latitude=-6.1751,
    #         longitude=106.8272,
    #     ),
    # )

    # competitor = Competitor(
    #     analysis_date=datetime.now(),
    #     name="Toko XYZ",
    #     industry="Retail",
    #     google_maps_rating=4.0,
    #     competitor_type=CompetitorType.DIRECT,
    #     google_maps_number_of_reviews=100,
    #     google_maps_url="https://maps.google.com/?q=Toko+XYZ",
    #     location=Location(
    #         address="Jl. Sudirman No. 456, Jakarta",
    #         subdistrict="Setiabudi",
    #         city="Jakarta Selatan",
    #         state="DKI Jakarta",
    #         country="Indonesia",
    #         latitude=-6.2248,
    #         longitude=106.8090,
    #     ),
    # )

    # print(business)
    # print(competitor)

    print(Business.model_json_schema())
