from flask import Flask, request, jsonify, make_response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
		"https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# refer - https://www.geeksforgeeks.org/using-google-sheets-as-database-in-python/

# Assign credentials ann path of style sheet
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("alt-project-demo").sheet1


app = Flask(__name__)

# create API endpoints

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/api/v1/get', methods=['GET'])
def get_data():
    data = sheet.get_all_records()
    print(data)
    return make_response(jsonify({'response': data, 'message':  'retrieved data'}), 200)

@app.route('/api/v1/get/<id>', methods=['GET'])
def get_data_by_id(id):
    print(id)
    # refer docs - https://docs.gspread.org/en/latest/user-guide.html#selecting-a-worksheet
    # get all records, then filter ...
    data = sheet.get_all_records()
    print(data)
    # refer list comprehension - https://www.programiz.com/python-programming/list-comprehension
    refined = [row for row in data if row["id"]==int(id)]
    return make_response(jsonify({'response': refined, 'message':  'retrieved data for {}'.format(id)}), 200)

@app.route('/api/v1/post', methods=['POST'])
def post_data():
    data = request.get_json()
    print(data)
    row = [data["id"], data["name"], data["score"]]  # TODO add error handling
    sheet.append_row(row)
    return make_response(jsonify({'response': data, 'message': 'inserted data'}), 200)

# dummy methods. TODO implement functionality
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

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    port = int(os.getenv('PORT'))
    app.run(threaded=True, port=port)
