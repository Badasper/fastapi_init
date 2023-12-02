from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_logging_ex.routers import api_router, api_router_dev
from fastapi_logging_ex.settings import app_logger, settings


def get_application():
    _app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        openapi_url=settings.OPENAPI_URL,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )

    _app.include_router(api_router, prefix=settings.API_PREFIX)
    if settings.ADD_DEV_ROUTERS:
        _app.include_router(api_router_dev, prefix=settings.API_PREFIX)
    app_logger.info("Congrutulation! Application start...")

    return _app


app = get_application()
