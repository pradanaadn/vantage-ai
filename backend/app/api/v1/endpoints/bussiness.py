from fastapi import APIRouter, status


router = APIRouter()


@router.post("/{business_id}")
def get_business_info(business_id: str):
    pass


@router.post("/{business_id}/analyze")
def analyze_bussiness(business_id: str):
    pass


@router.get("/{business_id}/analyze")
def analyze_competitors(business_id: str):
    pass


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_business():
    pass


@router.put("/{business_id}")
def update_business(business_id: str):
    pass


@router.delete("/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business(business_id: str):
    pass


@router.get("/{business_id}/competitors")
def get_competitors(business_id: str):
    pass


@router.post("/{business_id}/competitors", status_code=status.HTTP_201_CREATED)
def create_competitor(business_id: str):
    pass


@router.put("/competitors/{competitor_id}")
def delete_competitor(competitor_id: str):
    pass
