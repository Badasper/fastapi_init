from fastapi import APIRouter

from fastapi_logging_ex.apps.airport.routers import router as airports_router


api_router = APIRouter()

api_router_dev = APIRouter()  # for dev only

api_router.include_router(airports_router, prefix="/airports", tags=["Airports"])
