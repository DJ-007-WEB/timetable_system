import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app import app
except ImportError as exc:
    raise unittest.SkipTest(f"Application dependencies not installed: {exc}")


class ApiSecurityTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SESSION_COOKIE_SECURE=False)
        self.client = app.test_client()

    def test_csrf_token_endpoint(self):
        response = self.client.get("/csrf-token")
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrf_token", response.get_json())

    def test_mutating_request_requires_csrf(self):
        response = self.client.post("/logout")
        self.assertEqual(response.status_code, 403)

    def test_csrf_token_then_auth_check(self):
        response = self.client.get("/csrf-token")
        token = response.get_json()["csrf_token"]
        response = self.client.post("/logout", headers={"X-CSRF-Token": token})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
