from pydantic import BaseModel


class Country(BaseModel):
    name: str
    country_id: int
