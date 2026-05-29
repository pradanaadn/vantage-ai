import random

from datetime import timedelta, datetime
from typing import List, Union

from helpers.config_loader import load_json
from helpers.faker_helper import random_time

from generators.description_generator import (
    income_description,
    expense_description,
    variable_expense_description,
)

from generators.amount_generator import (
    generate_income_amount,
    generate_expense_amount,
)

from generators.payroll_generator import generate_payroll_transactions

from datatypes import (
    BusinessType,
    Scenario,
    StatementMode,
    Category,
    Transaction,
    as_key,
)


BUSINESSES = load_json("configs/businesses.json")

SCENARIOS = load_json("configs/scenarios.json")

RECURRENT_EXPENSE_KEYWORDS = (
    "admin",
    "listrik",
    "internet",
    "investasi",
    "langganan",
    "subscription",
    "sewa",
    "asuransi",
)

RECURRENT_EXPENSE_DAYS = {1, 15, 25}


def _is_recurrent_expense(description: str) -> bool:
    lowered = description.lower()
    return any(keyword in lowered for keyword in RECURRENT_EXPENSE_KEYWORDS)


def _pick_expense_description(
    expense_options: list[str],
    current_date: datetime,
) -> tuple[str, bool]:
    recurrent_options = [
        description for description in expense_options if _is_recurrent_expense(description)
    ]
    variable_options = [
        description for description in expense_options if not _is_recurrent_expense(description)
    ]

    if current_date.day in RECURRENT_EXPENSE_DAYS and recurrent_options:
        return random.choice(recurrent_options), True

    if variable_options:
        return random.choice(variable_options), False

    chosen = random.choice(expense_options)
    return chosen, _is_recurrent_expense(chosen)


def generate_transactions(
    business_type: Union[str, BusinessType],
    scenario: Union[str, Scenario],
    statement_mode: Union[str, StatementMode],
    start_date: datetime,
    days: int,
    starting_balance: int,
) -> List[Transaction]:

    business_key = as_key(business_type)
    scenario_key = as_key(scenario)
    mode_key = as_key(statement_mode)

    business_config = BUSINESSES[business_key]
    scenario_config = SCENARIOS[scenario_key]

    current_balance: int = starting_balance

    transactions: List[Transaction] = []

    for day in range(days):

        current_date = start_date + timedelta(days=day)

        # =====================================================
        # PAYROLL
        # =====================================================

        if current_date.day in [25, 26]:

            payroll_txs, current_balance = generate_payroll_transactions(
                current_date, current_balance
            )

            transactions.extend(payroll_txs)

        # =====================================================
        # DAILY TX COUNT
        # =====================================================

        daily_count = random.randint(2, 8)

        for _ in range(daily_count):

            # =================================================
            # CATEGORY
            # =================================================

            if mode_key == StatementMode.INCOME.value:
                category = Category.INCOME.value

            elif mode_key == StatementMode.OPEX.value:
                category = Category.OPEX.value

            elif mode_key == StatementMode.CAPEX.value:
                category = Category.CAPEX.value

            else:

                rand = random.random()

                if rand < 0.65:
                    category = Category.INCOME.value

                elif rand < 0.9:
                    category = Category.OPEX.value

                else:
                    category = Category.CAPEX.value

            # =================================================
            # AMOUNT
            # =================================================

            if category == Category.INCOME.value:

                tx_type = "CR"

                amount = generate_income_amount(scenario_config)

                current_balance += amount

            else:

                tx_type = "DB"

                amount = generate_expense_amount(scenario_config)

                current_balance -= amount

            # =================================================
            # DESCRIPTION
            # =================================================

            if category == Category.INCOME.value:

                base_desc = random.choice(business_config[category])
                desc = income_description(base_desc)

            else:
                base_desc, is_recurrent_expense = _pick_expense_description(
                    business_config[category], current_date
                )
                desc = (
                    expense_description(base_desc)
                    if is_recurrent_expense
                    else variable_expense_description(base_desc)
                )


            # =================================================
            # APPEND
            # =================================================

            transactions.append(
                {
                    "datetime": current_date.strftime("%d/%m/%Y")
                    + f" {random_time()}",
                    "desc": desc,
                    "type": tx_type,
                    "category": category,
                    "amount": amount,
                    "balance": current_balance,
                }
            )

    return sorted(transactions, key=lambda x: x["datetime"])