from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class TransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionCategory(str, Enum):
    PENDAPATAN_OPERASIONAL = "Pendapatan Operasional"
    PENDAPATAN_NON_OPERASIONAL = "Pendapatan Non-Operasional"
    INFLOW_NON_PENDAPATAN = "Inflow Non-Pendapatan"
    COGS = "Beban Pokok Penjualan (COGS)"
    OPEX = "Beban Operasional (OPEX)"
    CAPEX = "Belanja Modal (CAPEX)"
    BEBAN_NON_OPERASIONAL = "Beban Non-Operasional"
    OUTFLOW_NON_BEBAN = "Outflow Non-Beban"
    UNCLASSIFIED = "Belum Terklasifikasi"


class FinancialHealth(str, Enum):
    VERY_HEALTHY = "very_healthy"
    HEALTHY = "healthy"
    MODERATE = "moderate"
    AT_RISK = "at_risk"
    DISTRESSED = "distressed"


class Transaction(BaseModel):
    date: datetime = Field(..., description="Tanggal transaksi")
    description: str = Field(..., description="Deskripsi transaksi")
    type: TransactionType = Field(..., description="Tipe transaksi: credit atau debit")
    category: TransactionCategory = Field(..., description="Kategori transaksi")
    subcategory: str | None = Field(None, description="Subkategori transaksi")
    amount: float = Field(..., description="Jumlah transaksi")
    balance: float = Field(..., description="Saldo akhir")
    reference: str | None = Field(None, description="Referensi transaksi")


class BankStatement(BaseModel):
    name: str = Field(..., description="Nama pemilik rekening")
    account_number: str = Field(..., description="Nomor rekening")
    period_start: datetime = Field(..., description="Tanggal awal periode")
    period_end: datetime = Field(..., description="Tanggal akhir periode")
    currency: str = Field(..., description="Mata uang")
    initial_balance: float = Field(..., description="Saldo awal")
    final_balance: float = Field(..., description="Saldo akhir")
    transactions: list[Transaction] = Field(
        ..., description="Daftar transaksi dalam periode"
    )

    def amount_by_category(self) -> dict[str, float]:
        """Menghitung total jumlah per kategori transaksi."""
        totals = {}
        for txn in self.transactions:
            if txn.category not in totals:
                totals[txn.category] = 0.0
            totals[txn.category] += txn.amount
        return totals

    def amount_by_category_and_day_date(self) -> dict[str, dict[str, float]]:
        """Menghitung total jumlah per kategori transaksi per tanggal."""
        totals = {}
        for txn in self.transactions:
            date_str = txn.date.strftime("%Y-%m-%d")
            if date_str not in totals:
                totals[date_str] = {}
            if txn.category not in totals[date_str]:
                totals[date_str][txn.category] = 0.0
            totals[date_str][txn.category] += txn.amount
        return totals


class FinancialReport(BaseModel):
    file_url: str = Field(..., description="URL file laporan keuangan")
    bank_statement: BankStatement | None = Field(
        ..., description="Data bank statement yang diproses"
    )
    generated_at: datetime = Field(..., description="Waktu laporan keuangan dibuat")
    created_at: datetime = Field(
        ..., description="Waktu laporan keuangan disimpan dalam sistem"
    )

    def amount_by_category(self) -> dict[str, float]:
        """Menghitung total jumlah per kategori transaksi dari bank statement."""
        if self.bank_statement:
            return self.bank_statement.amount_by_category()
        return {}

    def amount_by_category_and_day_date(self) -> dict[str, dict[str, float]]:
        """Menghitung total jumlah per kategori transaksi per tanggal dari bank statement."""
        if self.bank_statement:
            return self.bank_statement.amount_by_category_and_day_date()
        return {}


class FinancialAnalysis(BaseModel):
    report_id: str = Field(..., description="ID laporan keuangan yang dianalisis")
    insights: list[str] = Field(
        ..., description="Daftar insight dari analisis laporan keuangan"
    )
    warnings: list[str] = Field(
        ..., description="Daftar peringatan dari analisis laporan keuangan"
    )
    health_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Skor kesehatan keuangan berdasarkan analisis laporan keuangan",
    )
    health_status: FinancialHealth | None = Field(
        None,
        description="Status kesehatan keuangan berdasarkan analisis laporan keuangan",
    )
    recommendations: list[str] = Field(
        ..., description="Daftar rekomendasi berdasarkan analisis laporan keuangan"
    )

    @model_validator(mode="after")
    def validate_health_status(self) -> "FinancialAnalysis":
        expected = _status_from_score(self.health_score)
        self.health_status = expected
        return self


def _status_from_score(score: float) -> FinancialHealth:
    if score >= 80:
        return FinancialHealth.VERY_HEALTHY
    if score >= 70:
        return FinancialHealth.HEALTHY
    if score >= 60:
        return FinancialHealth.MODERATE
    if score >= 40:
        return FinancialHealth.AT_RISK
    return FinancialHealth.DISTRESSED
