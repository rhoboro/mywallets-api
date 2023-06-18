from fastapi import FastAPI
from app.api import router as api_router
from app.exceptions import init_exception_handler
from app.log import init_log
from app.middlewares import init_middlewares

app = FastAPI(title="MyWallets API")
init_log()
init_exception_handler(app)
init_middlewares(app)
app.include_router(api_router, prefix="/api")
