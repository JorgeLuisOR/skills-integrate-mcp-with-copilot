import unittest

from fastapi.testclient import TestClient

from src.app import app


class AdminModeTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_signup_requires_teacher_authentication(self):
        response = self.client.post(
            "/activities/Chess Club/signup?email=student@mergington.edu"
        )
        self.assertEqual(response.status_code, 403)

    def test_teacher_login_accepts_known_credentials(self):
        response = self.client.post(
            "/auth/login",
            json={"username": "teacher", "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_teacher_can_signup_when_authenticated(self):
        login_response = self.client.post(
            "/auth/login",
            json={"username": "teacher", "password": "password123"},
        )
        token = login_response.json()["token"]

        response = self.client.post(
            "/activities/Chess Club/signup?email=student@mergington.edu",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
