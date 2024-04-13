from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.base import BaseTestCase
from vendingmachine.user.enums import RoleName


class TestEngineRoutes(BaseTestCase):
    def test_two_user_deposit_coins_but_only_one_allowed(self, client: TestClient, session: Session):
        user_1_token = self.create_user_and_get_auth_token(
            client=client,
            session=session,
            username="user_1",
            password="password",
            role=RoleName.BUYER,
        )
        user_2_token = self.create_user_and_get_auth_token(
            client=client,
            session=session,
            username="user_2",
            password="password",
            role=RoleName.BUYER,
        )
        response = client.post(
            "/deposit/",
            headers={"Authorization": f"Bearer {user_1_token}"},
            json={"coin_type": "TWENTY", "quantity": 1},
        )
        expected_response = {
            "coin_type": "TWENTY",
            "quantity": 1,
            "message": "Coins deposited successfully.",
            "total_deposited": {"five": 0, "ten": 0, "twenty": 1, "fifty": 0, "hundred": 0},
        }
        assert response.status_code == 200
        assert response.json() == expected_response

        # Another buyer calls this endpoint
        response_2 = client.post(
            "/deposit/",
            headers={"Authorization": f"Bearer {user_2_token}"},
            json={"coin_type": "TWENTY", "quantity": 1},
        )
        assert response_2.status_code == 422
        assert response_2.json() == {"detail": "Machine is in use by another user"}
