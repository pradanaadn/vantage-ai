from prefect import flow


@flow(name="test-categorize-bank-statement", log_prints=True)
def test_categorize_bank_statement(
    bussiness_id: str,
) -> None:
    print(f"Running test categorize bank statement flow for business ID: {bussiness_id}")
    
    
if __name__ == "__main__":
    test_categorize_bank_statement.serve()