import pandas as pd

from datetime import datetime, timedelta
from typing import Union

from generators.transaction_generator import generate_transactions
from generators.pdf_generator import generate_pdf

from datatypes import BusinessType, Scenario, StatementMode
from typing import Literal

def create_synthetic_bank_statement(
    account_name: str = "PT Kopi Nusantara",
    account_number: str = "9988776655",
    bank_name: str = "BANK NUSANTARA",
    business_type: Union[str, BusinessType] = BusinessType.COFFEE_SHOP,
    scenario: Union[str, Scenario] = Scenario.HEALTHY,
    statement_mode: Union[str, StatementMode] = StatementMode.MIXED,
    start_date_str: str = "2026-07-01",
    days: int = 30,
    starting_balance: int = 75_000_000,
    output_pdf_path: str = "output/statement.pdf",
    template: Literal['classic', "type"] = "classic",
    output_csv_path: str = "output/statement.csv",
) -> None:

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    transactions = generate_transactions(
        business_type=business_type,
        scenario=scenario,
        statement_mode=statement_mode,
        start_date=start_date,
        days=days,
        starting_balance=starting_balance,
    )

    # compute period text from start_date and days
    end_date = start_date + timedelta(days=days - 1)

    months_id = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember",
    }

    if start_date.year == end_date.year:
        if start_date.month == end_date.month:
            period = f"{months_id[start_date.month]} {start_date.year}"
        else:
            period = f"{months_id[start_date.month]} - {months_id[end_date.month]} {start_date.year}"
    else:
        period = f"{start_date.day} {months_id[start_date.month]} {start_date.year} - {end_date.day} {months_id[end_date.month]} {end_date.year}"

    # =====================================================
    # CSV
    # =====================================================

    pd.DataFrame(transactions).to_csv(output_csv_path, index=False)

    # =====================================================
    # PDF
    # =====================================================

    generate_pdf(
        transactions=transactions,
        business_type=business_type,
        scenario=scenario,
        account_name=account_name,
        account_number=account_number,
        bank_name=bank_name,
        period=period,
        starting_balance=starting_balance,
        output_pdf_path=output_pdf_path,
        template=template,
    )

    print("DONE")


if __name__ == "__main__":
    create_synthetic_bank_statement(
        business_type=BusinessType.COFFEE_SHOP,
        scenario=Scenario.HEALTHY,
        statement_mode=StatementMode.MIXED,
        template="type",
    )
