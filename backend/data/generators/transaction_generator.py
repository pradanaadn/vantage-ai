import random

from datetime import timedelta, datetime
from typing import List, Union

from helpers.config_loader import load_json
from helpers.faker_helper import random_time

from generators.description_generator import (
    income_description,
    expense_description,
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

            base_desc = random.choice(business_config[category])

            if category == Category.INCOME.value:

                desc = income_description(base_desc)

            else:

                desc = expense_description(base_desc)

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