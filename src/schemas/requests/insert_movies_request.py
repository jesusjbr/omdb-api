from pydantic import BaseModel


class InsertTitleBody(BaseModel):
    title: str
