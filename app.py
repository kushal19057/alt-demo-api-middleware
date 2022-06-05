from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# create API endpoints

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/v1/get', methods=['GET'])
def get_data():
    return make_response(jsonify({'response': {}, 'message':  'retrieved data'}), 200)

@app.route('/api/v1/get/<id>', methods=['GET'])
def get_data_by_id(id):
    print(id)
    return make_response(jsonify({'response': {}, 'message':  'retrieved data for {}'.format(id)}), 200)

@app.route('/api/v1/post', methods=['POST'])
def post_data():
    data = request.get_json()
    print(data)
    return make_response(jsonify({'response': data, 'message': 'inserted data'}), 200)

@app.route('/api/v1/put/<id>', methods=['PUT'])
def put_data_by_id(id):
    print(id)
    data = request.get_json()
    print(data)
    return make_response(jsonify({'response': data, 'message': 'updated data for {}'.format(id)}), 200)

@app.route('/api/v1/delete/<id>', methods=['DELETE'])
def delete_data_by_id(id):
    print(id)
    return make_response(jsonify({'response': {}, 'message': 'deleted data for {}'.format(id)}), 200)

# references :
# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
# https://www.section.io/engineering-education/flask-crud-api/
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
# test endpoints using postman on localhost
