from fastapi import APIRouter

from fastapi_logging_ex.apps.airport.service import AirportService


router = APIRouter()


@router.get("/{country_id}")
def get_airports_ids(country_id: int):
    return AirportService().get_airports_ids(country_id=country_id)
