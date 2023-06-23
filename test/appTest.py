import app
from test_base import BaseTestCase


class AppTest(BaseTestCase):

    def test_search_jokes_id(self):
        response = self.client.get('/api/jokes/1')
        self.assert200(response)
        self.assertEqual(response.json, {
            'id': 1,
            'value': 'Joke 1',
            'created_at': '2023-06-22 03:22:28',
            'updated_at': '2023-06-23 13:42:28',
            'removed': False,
            'type': 'Joke'
        })

    def test_search_jokes(self):
        response = self.client.get('/jokes/?query=frappuccino')
        self.assert200(response)
        self.assertEqual(response.json, [
            [
                "Chuck Norris ordered egg fu yung, a banana split and a frappuccino at the local KFC "
                "and got it along with a complementary platter of lobster thermidor."
            ]
        ])

    def test_create_jokes(self):
        joke = {
            'value': 'test joke',
            'created_at': '2023-04-22 03:22:28',
            'updated_at': '2023-05-23 13:42:28',
            'removed': False
        }
        response = self.client.post('/api/jokes/', json=joke)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['value'], 'test joke')

    def test_update_joke(self):
        joke_id = 'KuzJeDStQQWymmvAUPV0Iw'
        updated_data = {'value': 'Joke is updated'}
        response = self.client.put(f'/api/jokes/{joke_id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['value'], 'Joke is updated')

        # Check if the joke content has been updated in the list
        joke = next((j for j in app.local_jokes if j.get_id() == joke_id), None)
        self.assertEqual(joke.get_value(), 'Joke is updated')
        self.assertEqual(joke.get_created_at(), '2020-01-05 13:42:28.664997')

    def test_delete_joke(self):
        joke_id = 2
        response = self.client.delete(f'/api/jokes/{joke_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], f'Joke deleted')

    def test_create_image_jokes(self):
        joke = {
            'value': 'test image joke',
            'removed': False,
            'url':'https://www.rd.com/wp-content',
        }
        response = self.client.post('/api/jokes/imageJoke/', json=joke)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['value'], 'test image joke')
        self.assertEqual(response.json['image_url'], 'https://www.rd.com/wp-content')
