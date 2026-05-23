from __future__ import annotations

from enum import Enum
from typing import TypedDict, List, Literal, Union, Any


class BusinessType(Enum):
    COFFEE_SHOP = "coffee_shop"
    RESTAURANT = "restaurant"
    TOKO_BUAH = "toko_buah"


class Scenario(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNSTABLE = "unstable"


class Category(Enum):
    INCOME = "income"
    OPEX = "opex"
    CAPEX = "capex"


class TxType(Enum):
    CR = "CR"
    DB = "DB"


class StatementMode(Enum):
    INCOME = "income"
    OPEX = "opex"
    CAPEX = "capex"
    MIXED = "mixed"


class Transaction(TypedDict):
    datetime: str
    desc: str
    type: Literal["CR", "DB"]
    category: str
    amount: int
    balance: int


TransactionList = List[Transaction]


def as_key(value: Union[str, Enum]) -> str:
    """Return the string key for an Enum or pass-through a str value.

    This helper keeps the rest of the code accepting either Enum members
    or plain strings for backwards compatibility.
    """

    return value.value if hasattr(value, "value") else str(value)
