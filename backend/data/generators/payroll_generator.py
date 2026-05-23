import random
from datetime import datetime
from typing import Tuple, List

from helpers.faker_helper import (
    person_name,
    reference,
)

from datatypes import Transaction


def generate_payroll_transactions(
    current_date: datetime, current_balance: int
) -> Tuple[List[Transaction], int]:
    transactions: List[Transaction] = []

    employee_count = random.randint(5, 20)

    for _ in range(employee_count):

        amount = random.randint(3_500_000, 9_000_000)

        current_balance -= amount

        transactions.append(
            {
                "datetime": current_date.strftime("%d/%m/%Y") + " 09:00:00",
                "desc": f"TF GAJI {person_name()} {reference()}",
                "type": "DB",
                "category": "opex",
                "amount": amount,
                "balance": current_balance,
            }
        )

    return transactions, current_balance