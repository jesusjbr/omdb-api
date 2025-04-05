from pydantic import BaseModel, conint


class Pagination(BaseModel):
    page: conint(ge=1) | None
    page_size: conint(ge=1, le=100)
