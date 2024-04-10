from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status

from vendingmachine import heartbeat
from vendingmachine.engine import routes as engine_routes
from vendingmachine.engine.exceptions import InvalidOperation
from vendingmachine.product import routes as product_routes
from vendingmachine.user import routes as user_routes

load_dotenv()
app = FastAPI(
    title="Vending Machine API",
    description="API for vending machine",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)
app.include_router(heartbeat.router)
app.include_router(user_routes.public_routes)
app.include_router(user_routes.authenticated_routes)
app.include_router(product_routes.authenticated_routes)
app.include_router(engine_routes.authenticated_routes)


@app.exception_handler(InvalidOperation)
def validation_exception_handler(request: Request, exc: InvalidOperation):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(exc),
    )
