from dotenv import load_dotenv
from fastapi import FastAPI

from vendingmachine import heartbeat
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
