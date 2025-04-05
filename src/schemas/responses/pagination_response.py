from pydantic import BaseModel


class PaginationResponse(BaseModel):
    """It serves as a template for other responses"""

    page: int
    page_size: int
    order_by: str
    order_type: str
    total: int
