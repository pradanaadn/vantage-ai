from fastapi import APIRouter, status


router = APIRouter()



@router.post("/bank-statement", status_code=status.HTTP_201_CREATED)
def upload_bank_statement(business_id: str):
    pass


@router.post("/bank-statement", status_code=status.HTTP_201_CREATED)
def get_financial_summary(business_id: str):
    pass


@router.post("/bank-statement", status_code=status.HTTP_201_CREATED)
def classify_bank_statement(business_id: str):
    pass


@router.post("/bank-statement", status_code=status.HTTP_201_CREATED)
def get_transaction_data(business_id: str):
    pass


@router.post("/bank-statement", status_code=status.HTTP_201_CREATED)
def get_classify_bank_statement(business_id: str):
    pass



@router.post("/bank-statement", status_code=status.HTTP_201_CREATED)
def analyze_financial_data(business_id: str):
    pass

@router.post("/bank-statement", status_code=status.HTTP_201_CREATED)
def get_financial_analyzes_result(business_id: str):
    pass
