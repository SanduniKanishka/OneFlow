import requests
from flask import Flask, jsonify


class Methods:

    def search_local_jokes(self, query, local_jokes):
        local_jokes_results = []
        for joke in local_jokes:
            if query.lower() in joke.get_value().lower() and not joke.get_removed():
                local_jokes_results.append(joke.get_value())
        return local_jokes_results

    def search_remote_jokes(self, query, local_jokes_ids):
        result = []
        # Base URL of the API
        base_url = 'https://api.chucknorris.io/jokes/search?'
        try:
            response = requests.get(base_url, params={'query': query})

            if response.status_code == 200:
                remote_jokes_results = response.json().get("result")
                for joke in remote_jokes_results:
                    if joke.get("id") not in local_jokes_ids:
                        result.append(joke.get("value"))
                return result

            else:
                return jsonify({'message': 'Failed to fetch remote data'}), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({'message': 'Error occurred while fetching remote data'}), 500

    def search_remote_jokes_by_id(self, joke_id, local_jokes_ids):
        try:
            url = "https://api.chucknorris.io/jokes/" + joke_id
            response = requests.get(url)

            if response.status_code == 200 and response.json().get("id") not in local_jokes_ids:
                return response.json()
            else:
                return []

        except requests.exceptions.RequestException as e:
            return jsonify({'message': 'Error occurred while fetching remote data'}), 500

    def search_local_jokes_by_id(self, joke_id, local_jokes):
        for joke in local_jokes:
            if str(joke.get_id()) == joke_id and not joke.get_removed():
                return joke
