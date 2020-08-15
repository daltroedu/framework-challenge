import json

from app.tests import TestBase


class TestPost(TestBase):
    def test_rest_api_v1_get_post(self):
        post = self.create_post()
        response = self.client.get(
            f'/api/v1/posts/{post.id}',
            headers=self.headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['title'], 'My Post')

    def test_rest_api_v1_get_all_posts(self):
        response = self.client.get(
            f'/api/v1/posts',
            headers=self.headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['_meta']['total_items'], 0)