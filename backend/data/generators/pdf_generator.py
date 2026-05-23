from weasyprint import HTML
from helpers.formatter import rupiah

from datetime import datetime
from typing import List, Union, Literal

from datatypes import Transaction, BusinessType, Scenario


def generate_pdf(
    transactions: List[Transaction],
    account_name: str,
    account_number: str,
    bank_name: str,
    period: str,
    business_type: Union[str, BusinessType],
    scenario: Union[str, Scenario],
    starting_balance: int,
    output_pdf_path: str,
    template: Literal["classic", "type"] = "classic",
) -> None:

    # =====================================================
    # SUMMARY
    # =====================================================

    total_db = sum(
        t["amount"]
        for t in transactions
        if t["type"] == "DB"
    )

    total_cr = sum(
        t["amount"]
        for t in transactions
        if t["type"] == "CR"
    )

    ending_balance = transactions[-1]["balance"]

    total_transactions = len(transactions)

    # avg_credit = (
    #     total_cr / max(
    #         len([t for t in transactions if t["type"] == "CR"]),
    #         1
    #     )
    # )

    # avg_debit = (
    #     total_db / max(
    #         len([t for t in transactions if t["type"] == "DB"]),
    #         1
    #     )
    # )
    # =====================================================
    # ROWS / HEADERS (support two templates)
    # =====================================================

    if template == "classic":
        header_columns_html = """
                <tr>

                    <th width="18%">Tanggal</th>

                    <th width="42%">Keterangan</th>

                    <th width="13%">Debet</th>

                    <th width="13%">Kredit</th>

                    <th width="14%">Saldo</th>

                </tr>
        """

    else:
        header_columns_html = """
                <tr>

                    <th width="18%">Tanggal</th>

                    <th width="42%">Keterangan</th>

                    <th width="10%">Tipe</th>

                    <th width="16%">Jumlah</th>

                    <th width="14%">Saldo</th>

                </tr>
        """

    rows_html = ""

    for idx, t in enumerate(transactions):

        row_class = "even-row" if idx % 2 == 0 else "odd-row"

        if template == "classic":
            db = rupiah(t["amount"]) if t["type"] == "DB" else ""
            cr = rupiah(t["amount"]) if t["type"] == "CR" else ""

            rows_html += f"""
        <tr class="{row_class}">
            <td>{t['datetime']}</td>

            <td>{t['desc']}</td>

            <td class="amount">{db}</td>

            <td class="amount">{cr}</td>

            <td class="amount">
                {rupiah(t['balance'])}
            </td>
        </tr>
        """

        else:
            type_col = t["type"]
            amt = rupiah(t["amount"])

            rows_html += f"""
        <tr class="{row_class}">
            <td>{t['datetime']}</td>

            <td>{t['desc']}</td>

            <td class="amount">{type_col}</td>

            <td class="amount">{amt}</td>

            <td class="amount">{rupiah(t['balance'])}</td>
        </tr>
        """

    generated_at = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    # prepare saldo awal row depending on template
    first_dt = transactions[0]["datetime"] if transactions else ""

    if template == "classic":
        saldo_awal_row = f"""
                <tr>

                    <td>
                        {first_dt}
                    </td>

                    <td>
                        <b>SALDO AWAL</b>
                    </td>

                    <td></td>

                    <td></td>

                    <td class="amount">
                        <b>{rupiah(starting_balance)}</b>
                    </td>

                </tr>
        """

    else:
        saldo_awal_row = f"""
                <tr>

                    <td>
                        {first_dt}
                    </td>

                    <td>
                        <b>SALDO AWAL</b>
                    </td>

                    <td></td>

                    <td class="amount"></td>

                    <td class="amount">
                        <b>{rupiah(starting_balance)}</b>
                    </td>

                </tr>
        """

    # =====================================================
    # HTML
    # =====================================================

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="utf-8">

        <style>

            @page {{
                size: A4;
                margin: 15mm;
            }}

            body {{
                font-family: Arial, sans-serif;
                font-size: 10px;
                color: #222;
            }}

            .header {{
                border-bottom: 3px solid #003b70;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}

            .bank-name {{
                font-size: 24px;
                font-weight: bold;
                color: #003b70;
            }}

            .statement-title {{
                float: right;
                font-size: 18px;
                font-weight: bold;
                margin-top: -28px;
                color: #003b70;
            }}

            .section-title {{
                background: #003b70;
                color: white;
                padding: 6px;
                font-weight: bold;
                margin-top: 20px;
            }}

            .info-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}

            .info-table td {{
                padding: 5px;
                border-bottom: 1px solid #ddd;
            }}

            .summary-box {{
                background: #f5f7fa;
                border: 1px solid #d6dce5;
                padding: 12px;
                margin-top: 15px;
            }}

            table.tx-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}

            table.tx-table th {{
                background: #003b70;
                color: white;
                padding: 8px;
                font-size: 10px;
            }}

            table.tx-table td {{
                border: 1px solid #ddd;
                padding: 6px;
                vertical-align: top;
            }}

            .amount {{
                text-align: right;
            }}

            .even-row {{
                background: #fafafa;
            }}

            .odd-row {{
                background: white;
            }}

            .footer {{
                margin-top: 30px;
                font-size: 9px;
                color: #666;
                border-top: 1px solid #ccc;
                padding-top: 10px;
            }}

            .bottom-summary {{
                margin-top: 20px;
                border: 1px solid #ddd;
            }}

            .bottom-summary td {{
                padding: 8px;
                border: 1px solid #ddd;
            }}

            .summary-label {{
                background: #f2f2f2;
                font-weight: bold;
                width: 40%;
            }}

        </style>

    </head>

    <body>

        <!-- HEADER -->

        <div class="header">

            <div class="bank-name">
                {bank_name}
            </div>

            <div class="statement-title">
                REKENING KORAN
            </div>

        </div>

        <!-- CUSTOMER INFO -->

        <div class="section-title">
            INFORMASI NASABAH
        </div>

        <table class="info-table">

            <tr>
                <td width="20%"><b>Nama Rekening</b></td>
                <td width="30%">{account_name}</td>

                <td width="20%"><b>No Rekening</b></td>
                <td width="30%">{account_number}</td>
            </tr>

            <tr>
                <td><b>Periode</b></td>
                <td>{period}</td>

                <td><b>Mata Uang</b></td>
                <td>IDR</td>
            </tr>


        </table>

        <!-- SUMMARY moved to bottom -->

        <!-- TRANSACTION TABLE -->

        <div class="section-title">
            DETAIL TRANSAKSI
        </div>

        <table class="tx-table">


                <thead>
                    {header_columns_html}
                </thead>

                <tbody>

                    {saldo_awal_row}

                    {rows_html}

                </tbody>

        </table>

        <!-- BOTTOM SUMMARY -->

        <div class="section-title">
            RINGKASAN REKENING
        </div>

        <table class="bottom-summary" width="100%">

            <tr>
                <td class="summary-label">Saldo Awal</td>
                <td>Rp {rupiah(starting_balance)}</td>
            </tr>

            <tr>
                <td class="summary-label">Total Debet</td>
                <td>Rp {rupiah(total_db)}</td>
            </tr>

            <tr>
                <td class="summary-label">Total Kredit</td>
                <td>Rp {rupiah(total_cr)}</td>
            </tr>

            <tr>
                <td class="summary-label">Saldo Akhir</td>
                <td>Rp {rupiah(ending_balance)}</td>
            </tr>

            <tr>
                <td class="summary-label">Total Transaksi</td>
                <td>{total_transactions} transaksi</td>
            </tr>

        </table>

        <!-- FOOTER -->

        <div class="footer">

            Dokumen ini dihasilkan secara otomatis untuk simulasi data sintetis.

            <br><br>

            Generated at:
            {generated_at}

        </div>

    </body>

    </html>
    """

    HTML(
        string=html
    ).write_pdf(output_pdf_path)