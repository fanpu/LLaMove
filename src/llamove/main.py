from fastapi import FastAPI
from llamove.api.routes.api import router as api_router
from llamove.core import config
from loguru import logger


def get_app() -> FastAPI:
    app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG)
    app.include_router(api_router, prefix=config.API_PREFIX)

    logger.info(f"Starting {config.PROJECT_NAME}")

    return app


app = get_app()
