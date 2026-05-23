import random
from typing import List
from faker import Faker
from helpers.config_loader import load_json

fake = Faker("id_ID")

BANKS: List[str] = load_json("configs/banks.json")["banks"]


def person_name() -> str:
    return fake.name().upper()


def company_name() -> str:
    prefixes = ["PT", "CV", "UD"]

    return f"{random.choice(prefixes)} {fake.company().upper()}"


def bank_name() -> str:
    return random.choice(BANKS)


def reference() -> str:
    return f"REF-{random.randint(100000, 999999)}"


def random_time() -> str:
    hour = random.randint(7, 22)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return f"{hour:02}:{minute:02}:{second:02}"