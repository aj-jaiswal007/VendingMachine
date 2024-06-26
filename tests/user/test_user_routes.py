import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.base import BaseTestCase
from vendingmachine.user.models import User


class TestUserRoutes(BaseTestCase):
    def test_create_user(self, client: TestClient):
        response = client.post(
            "/users/",
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "jane.doe",
                "password": "password",
            },
        )
        expected_output_without_audit_fields = {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jane.doe",
            "role": "buyer",
        }
        print(json.dumps(response.json(), indent=4))
        assert response.status_code == 200
        response_json = response.json()
        response_json.pop("created_at")
        response_json.pop("updated_at")
        assert response_json == expected_output_without_audit_fields

    def test_get_token(self, client):
        # create a user
        create_response = client.post(
            "/users/",
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "jane.doe",
                "password": "password",
            },
        )
        assert create_response.status_code == 200
        # get the user
        response = client.post(
            "/token/",
            json={"username": "jane.doe", "password": "password"},
        )
        assert response.status_code == 200
        response_json = response.json()
        assert "access_token" in response_json

    def test_get_user(self, client):
        # create a user
        create_response = client.post(
            "/users/",
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "jane.doe",
                "password": "password",
            },
        )
        assert create_response.status_code == 200
        # get the user
        token_response = client.post(
            "/token/",
            json={"username": "jane.doe", "password": "password"},
        )
        assert token_response.status_code == 200
        token = token_response.json()["access_token"]
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        expected_output_without_audit_fields = {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jane.doe",
            "role": "buyer",
        }
        response_json = response.json()
        response_json.pop("created_at")
        response_json.pop("updated_at")
        assert response_json == expected_output_without_audit_fields

    def test_update_user(self, client: TestClient, session: Session):
        username = "jane.doe"
        password = "password"
        token = self.create_user_and_get_auth_token(
            client=client,
            session=session,
            username=username,
            password=password,
        )

        response = client.put(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
            json={"first_name": "Anthony", "last_name": "Gonzalves", "username": username},
        )
        assert response.status_code == 200
        expected_output_without_audit_fields = {
            "id": 1,
            "first_name": "Anthony",
            "last_name": "Gonzalves",
            "username": "jane.doe",
            "role": "buyer",
        }
        response_json = response.json()
        response_json.pop("created_at")
        response_json.pop("updated_at")
        assert response_json == expected_output_without_audit_fields

    def test_delete_user(self, client: TestClient, session: Session):
        auth_token = self.create_user_and_get_auth_token(
            client=client,
            session=session,
            username="jane.doe",
            password="password",
        )
        response = client.delete(
            "/users/me",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200

        user = session.query(User).filter(User.username == "jane.doe").first()
        assert not user.is_active, "User should be inactive"  # type: ignore
