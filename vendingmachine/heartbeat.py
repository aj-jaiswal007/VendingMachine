from fastapi import APIRouter

from vendingmachine.common.logger import logger

router = APIRouter()


@router.get("/heartbeat")
def heartbeat():
    logger.info("Heartbeat API called!")
    return {"status": "OK"}
