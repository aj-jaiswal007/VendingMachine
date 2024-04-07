from dotenv import load_dotenv
from fastapi import FastAPI
from vendingmachine import heartbeat


load_dotenv()
app = FastAPI()
app.include_router(heartbeat.router)
