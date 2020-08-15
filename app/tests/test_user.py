import json

from app.tests import TestBase


class TestUser(TestBase):
    def test_rest_api_v1_create_user(self):
        response = self.client.post(
            '/api/v1/users',
            headers=self.headers(),
            data=json.dumps(
                {
                    'email': 'admin@example.com',
                    'username': 'admin',
                    'password': 'admin',
                    'name': 'Admin'
                }
            )
        )
        self.assertEqual(response.status_code, 201)