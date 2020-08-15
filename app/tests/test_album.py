import json

from app.tests import TestBase


class TestAlbum(TestBase):
    def test_rest_api_v1_get_album(self):
        album = self.create_album()
        response = self.client.get(
            f'/api/v1/albums/{album.id}',
            headers=self.headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['title'], 'My Album')

    def test_rest_api_v1_get_all_albums(self):
        response = self.client.get(
            f'/api/v1/albums',
            headers=self.headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['_meta']['total_items'], 0)