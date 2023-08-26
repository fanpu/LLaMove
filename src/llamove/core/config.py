import logging
import sys

from llamove.core.logging import InterceptHandler
from loguru import logger
from starlette.config import Config

config = Config(".env")

PROJECT_NAME: str = "llamove"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
API_PREFIX: str = "/api"

# Logging configs
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
