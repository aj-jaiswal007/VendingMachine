from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from vendingmachine.user.enums import RoleName
from vendingmachine.user.models import User


class BaseTestCase:
    def create_user_and_get_auth_token(
        self,
        client: TestClient,
        session: Session,
        username: str,
        password: str,
        role: RoleName = RoleName.BUYER,
    ) -> str:
        create_response = client.post(
            "/users/",
            json={
                "first_name": "",
                "last_name": "",
                "username": username,
                "password": password,
            },
        )
        user_id = create_response.json()["id"]
        if role == RoleName.SELLER:
            # Need to update the role in DB directly
            session.query(User).filter(User.id == user_id).update({User.role: RoleName.SELLER})
            session.commit()

        response = client.post(
            "/token/",
            json={"username": username, "password": password},
        )
        response_json = response.json()
        return response_json["access_token"]
