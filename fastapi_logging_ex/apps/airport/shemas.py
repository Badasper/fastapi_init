from typing import List

from pydantic import BaseModel

from fastapi_logging_ex.apps.country.schemas import Country


class AirportId(BaseModel):
    airport_id: int


class AirportsShow(BaseModel):
    country: Country
    airports: List[AirportId]
    airports: List[AirportId]
