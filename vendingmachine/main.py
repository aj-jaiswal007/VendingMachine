from dotenv import load_dotenv
from fastapi import FastAPI
from vendingmachine import heartbeat
from vendingmachine.user import routes as user_routes


load_dotenv()
app = FastAPI()
app.include_router(heartbeat.router)
app.include_router(user_routes.router)
