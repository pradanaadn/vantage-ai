from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


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


class Transaction(BaseModel):
    date: datetime  = Field(..., description="Tanggal transaksi")
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
    transactions: list[Transaction] = Field(..., description="Daftar transaksi dalam periode")
