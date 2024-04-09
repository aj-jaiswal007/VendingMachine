from typing import Annotated

from fastapi import Depends, HTTPException, status

from vendingmachine.common.logger import logger

from .authentication import get_current_user_token
from .enums import RoleName
from .schemas import TokenData


class RoleChecker:
    def __init__(self, role):
        self.role = role

    def __call__(self, token_data: Annotated[TokenData, Depends(get_current_user_token)]):
        logger.info(f"Checking role {self.role} in {token_data.roles}")
        if self.role not in token_data.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )


allow_buyer = RoleChecker(RoleName.BUYER)
allow_seller = RoleChecker(RoleName.SELLER)
