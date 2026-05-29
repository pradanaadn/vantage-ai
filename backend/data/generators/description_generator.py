import random
from typing import List

from helpers.faker_helper import (
    person_name,
    company_name,
    bank_name,
    reference,
)


def income_description(base_desc: str) -> str:
    patterns: List[str] = [
        f"{base_desc} {reference()}",
        f"TRF DARI {person_name()} {bank_name()} {reference()}",
        f"QRIS {person_name()}",
        f"PEMBAYARAN {person_name()}",
        f"SETTLEMENT GOPAY {reference()}",
        f"SETTLEMENT SHOPEEPAY {reference()}",
        f"SETTLEMENT TOKOPEDIA {reference()}",
    ]

    return random.choice(patterns)


def expense_description(base_desc: str) -> str:
    return f"{base_desc} {reference()}"


def variable_expense_description(base_desc: str) -> str:
    patterns: List[str] = [
        f"{base_desc} {reference()}",
        f"TF KE {company_name()} {bank_name()} {reference()}",
        f"PEMBELIAN STOK {reference()}",
        f"PEMBAYARAN UTILITAS {reference()}",
    ]

    return random.choice(patterns)

