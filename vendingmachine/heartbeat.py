from typing import Annotated

from fastapi import APIRouter, Depends

from vendingmachine.common.logger import logger
from vendingmachine.settings import Settings, get_settings

router = APIRouter()


@router.get("/heartbeat")
def heartbeat(settings: Annotated[Settings, Depends(get_settings)]):
    logger.info("Heartbeat API called!")
    return {"status": "OK", "data": settings.model_dump(by_alias=True)}
