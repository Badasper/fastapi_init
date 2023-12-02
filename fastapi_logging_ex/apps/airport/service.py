from fastapi_logging_ex.apps.airport.shemas import AirportId, AirportsShow
from fastapi_logging_ex.apps.country.schemas import Country
from fastapi_logging_ex.settings import app_logger


class AirportService:
    def get_airports_ids(self, country_id: int) -> AirportsShow:
        # Do boilerplates with db and business logic
        app_logger.info("Get all Airports by Country ID")
        return AirportsShow(
            airports=[AirportId(airport_id=1), AirportId(airport_id=2)],
            country=Country(name="R", country_id=country_id),
        )
