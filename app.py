from flask import request
from datetime import datetime
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

import methods as methodsObj
import model.joke as joke_model

app = Flask(__name__)

local_jokes_ids = []
key_id = 0

local_jokes = [joke_model.Joke("", 'Joke 1', '2023-06-22 03:22:28', '2023-06-23 13:42:28', False),
               joke_model.Joke("", 'Joke 2', datetime.now(), datetime.now(), False)]


@app.route('/jokes/', methods=['GET'])
def search_jokes():
    query = request.args.get('query')
    jokes = []
    local_jokes_arr = methodsObj.Methods().search_local_jokes(query, local_jokes)
    remote_jokes_arr = methodsObj.Methods().search_remote_jokes(query, local_jokes_ids)
    if local_jokes_arr:
        jokes.append(local_jokes_arr)
    elif remote_jokes_arr:
        jokes.append(remote_jokes_arr)
    else:
        return jsonify("Joke does not exist"), 404

    return jsonify(jokes)


@app.route('/api/getAllLocalJokes/', methods=['GET'])
def get_all_local_jokes():
    local_jokes_results = []
    for joke in local_jokes:
        if not joke.get_removed():
            local_jokes_results.append(joke)
            local_jokes_results_json = [joke.__dict__ for joke in local_jokes_results]

    return jsonify(local_jokes_results_json), 201


@app.route('/api/jokes/<string:joke_id>', methods=['GET'])
def search_jokes_id(joke_id):
    jokes = []
    local_joke = methodsObj.Methods().search_local_jokes_by_id(joke_id, local_jokes)
    remote_joke = methodsObj.Methods().search_remote_jokes_by_id(joke_id, local_jokes_ids)
    if local_joke:
        jokes.append(local_joke)
        return jsonify(local_joke.__dict__)
    elif remote_joke:
        jokes.append(remote_joke)
        return jsonify(jokes)
    else:
        return jsonify("Joke does not exist")


@app.route('/api/jokes/', methods=['POST'])
def create_joke(self=None):
    data = request.get_json()
    value = data.get('value')
    new_joke = joke_model.Joke("", value, datetime.now(), datetime.now(), False)
    local_jokes.append(new_joke)
    local_jokes_ids.append(new_joke.get_id())
    return jsonify(new_joke.__dict__), 201


@app.route('/api/jokes/<string:joke_id>', methods=['PUT'])
def update_joke(joke_id):
    update_value = request.get_json().get('value')
    joke = methodsObj.Methods().search_remote_jokes_by_id(joke_id, local_jokes_ids)
    local_joke = update_local_joke(joke_id, update_value)
    if joke:
        joke['value'] = update_value
        joke['removed'] = False
        updated_joke = joke_model.Joke(joke['id'], request.get_json().get('value'),
                                       joke['created_at'], datetime.now(), False)
        local_jokes.append(updated_joke)
        local_jokes_ids.append(joke_id)
        return jsonify(updated_joke.__dict__)
    elif local_joke:
        return jsonify(local_joke.__dict__)
    else:
        return jsonify({'message': '404 not found'}), 404


def update_local_joke(joke_id, new_value):
    for joke in local_jokes:
        if str(joke.get_id()) == joke_id:
            joke.set_value(new_value)
            return joke

    return None


@app.route('/api/jokes/<string:joke_id>', methods=['DELETE'])
def delete_joke(joke_id):
    local_joke = methodsObj.Methods().search_local_jokes_by_id(joke_id, local_jokes)
    joke_exit_flag = 0
    if local_joke:
        local_joke.set_removed(True)
        joke_exit_flag = 1

    remote_joke = methodsObj.Methods().search_remote_jokes_by_id(joke_id, local_jokes_ids)
    if remote_joke:
        remote_joke_model = joke_model.Joke(remote_joke['id'], remote_joke['value'], remote_joke['created_at'],
                                            remote_joke['updated_at'], True)
        local_jokes.append(remote_joke_model)
        joke_exit_flag = 1
        local_jokes_ids.append(remote_joke_model.get_id())

    if joke_exit_flag == 1:
        return jsonify({'message': 'Joke deleted'}), 200
    else:
        return jsonify({'message': 'Joke not found'}), 404


@app.route('/api/jokes/imageJoke/', methods=['POST'])
def create_image_joke(self=None):
    data = request.get_json()
    value = data.get('value')
    url = data.get('url')
    image_joke = joke_model.ImageJoke("", value, datetime.now(), datetime.now(), False, url)
    local_jokes.append(image_joke)
    local_jokes_ids.append(image_joke.get_id())
    return jsonify(image_joke.__dict__), 201


@app.route('/api/swagger')
def swagger_docs():
    swag = {
        'swagger': '2.0',
        'info': {
            'title': 'Your API Documentation Title',
            'version': '1.0',
        },
        'paths': {
            '/api/jokes/{jokeId}': {
                'get': {
                    'parameters': [
                        {
                            'name': 'jokeId',
                            'in': 'path',
                            'type': 'string',
                            'required': True,
                            'description': 'The ID of the joke',
                        },
                    ],
                    'responses': {
                        '200': {
                            'description': 'The joke object',
                            'schema': {
                                '$ref': '#/definitions/Joke',
                            },
                        },
                        '404': {
                            'description': 'Joke not found',
                        },
                    },
                },
            },
            '/api/jokes/': {
                'post': {
                    'parameters': [
                        {
                            'name': 'joke',
                            'in': 'body',
                            'required': True,
                            'schema': {
                                '$ref': '#/definitions/JokeModel',
                            },
                            'x-internal': True,
                        },
                    ],
                    'responses': {
                        '201': {
                            'description': 'Joke created successfully',
                        },
                        '400': {
                            'description': 'Invalid request payload',
                        },
                    },
                },
            },
            '/jokes': {
                'get': {
                    'parameters': [
                        {
                            'name': 'query',
                            'in': 'query',
                            'type': 'string',
                            'required': True,
                            'description': 'The query of the joke',
                        },
                    ],
                    'responses': {
                        '200': {
                            'description': 'The joke object',
                            'schema': {
                                'type': 'array',
                                'items': {
                                    '$ref': '#/definitions/Joke',
                                }

                            },
                        },
                        '404': {
                            'description': 'Joke does not exist',
                        },
                    },
                },
            },
            '/api/jokes/{joke_id}': {
                'put': {
                    'parameters': [
                        {
                            'name': 'joke_id',
                            'in': 'path',
                            'type': 'string',
                            'required': True,
                            'description': 'The ID of the joke',
                        },
                        {
                            'name': 'body',
                            'in': 'body',
                            'description': 'New joke value',
                            'required': True,
                            'schema': {
                                '$ref': '#/definitions/JokeModel'
                            }
                        },
                    ],
                    'responses': {
                        '200': {
                            'description': 'The joke object',
                            'schema': {
                                '$ref': '#/definitions/Joke',
                            },
                        },
                        '404': {
                            'description': 'Joke not found',
                        },
                    },
                },
            },
            '/api/jokes/{jokeid}': {
                'delete': {
                    'parameters': [
                        {
                            'name': 'jokeid',
                            'in': 'path',
                            'type': 'string',
                            'required': True,
                            'description': 'The ID of the joke',
                        },
                    ],
                    'responses': {
                        '200': {
                            'description': 'Joke deleted',
                        },
                        '404': {
                            'description': 'Joke not found',
                        },
                    },
                },
            },
            '/api/jokes/imageJoke/': {
                'post': {
                    'parameters': [
                        {
                            'name': 'joke',
                            'in': 'body',
                            'required': True,
                            'schema': {
                                '$ref': '#/definitions/ImageJoke',
                            },
                            'x-internal': True,
                        },
                    ],
                    'responses': {
                        '201': {
                            'description': 'Joke created successfully',
                        },
                        '400': {
                            'description': 'Invalid request payload',
                        },
                    },
                },
            },
            '/api/getAllLocalJokes/': {
                'get': {
                    'responses': {
                        '200': {
                            'description': 'The joke object',
                            'schema': {
                                'type': 'array',
                                'items': {
                                    '$ref': '#/definitions/Joke',
                                }
                            },
                        },
                        '404': {
                            'description': 'Joke not found',
                        },
                    },
                },
            },
        },

        'definitions': {
            'Joke': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                    },
                    'value': {
                        'type': 'string',
                    },
                    'created_at': {
                        'type': 'string',
                    },
                    'updated_at': {
                        'type': 'string',
                    },
                    'removed': {
                        'type': 'boolean',
                    },
                },
            },
            'JokeModel': {
                'type': 'object',
                'properties': {
                    'value': {
                        'type': 'string',
                    },
                },
                'required': ['value']
            },
            'ImageJoke': {
                'type': 'object',
                'properties': {
                    'value': {
                        'type': 'string',
                    },
                    'url': {
                        'type': 'string',
                    }
                },
            },

        },
    }
    return jsonify(swag)


# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # URL for accessing Swagger UI
API_URL = '/api/swagger'  # URL for accessing Swagger JSON

# Create Swagger UI blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API Documentation"  # Display name for the API
    }
)

# Register Swagger UI blueprint
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
