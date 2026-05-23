import random
from typing import Mapping, Any


def generate_income_amount(scenario_config: Mapping[str, Any]) -> int:
    return random.randint(
        scenario_config["income_range"][0],
        scenario_config["income_range"][1],
    )


def generate_expense_amount(scenario_config: Mapping[str, Any]) -> int:
    return random.randint(
        scenario_config["expense_range"][0],
        scenario_config["expense_range"][1],
    )