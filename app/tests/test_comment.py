import json

from app.tests import TestBase


class TestComment(TestBase):
    def test_rest_api_v1_get_comment(self):
        comment = self.create_comment()
        response = self.client.get(
            f'/api/v1/comments/{comment.id}',
            headers=self.headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['contents'], 'My Comment')

    def test_rest_api_v1_get_all_comments(self):
        response = self.client.get(
            f'/api/v1/posts',
            headers=self.headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['_meta']['total_items'], 0)