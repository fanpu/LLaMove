from fastapi import APIRouter
from llamove.api.routes import health_check

router = APIRouter()

for route, tags in [(health_check.router, ["health_check"])]:
    router.include_router(route, tags=tags, prefix="/v1")
