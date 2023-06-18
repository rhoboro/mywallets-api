import logging
from app.utils.datetime import utcnow

logger = logging.getLogger(__name__)

def init_middlewares(app) -> None:
    @app.middleware("http")
    async def log_middleware(request, call_next):
        st = utcnow()
        response = await call_next(request)
        et = utcnow()
        logger.info(
            "processing time: %f",
            (et - st).total_seconds())
        return response
