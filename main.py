import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# refer - https://www.geeksforgeeks.org/using-google-sheets-as-database-in-python/

# Assign credentials ann path of style sheet
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("alt-project-demo").sheet1

# define API routes
@app.get("/")
async def index():
    return {"data": "Hi there! Try the GET and POST routes :)"}

@app.get("/api/v1/get")
async def get_data():
    data = sheet.get_all_records()
    print(data)
    return {"data": data}

@app.get("/api/v1/get/{id}")
async def get_data_by_id(id: int):
    # refer docs - https://docs.gspread.org/en/latest/user-guide.html#selecting-a-worksheet
    # get all records, then filter ...
    data = sheet.get_all_records()
    # refer list comprehension - https://www.programiz.com/python-programming/list-comprehension
    refined = [row for row in data if row["id"]==int(id)]
    return {'data': refined}

class User(BaseModel):
    id: int
    name: str
    score: int

@app.post("/api/v1/post/")
async def create_data(user: User):
    row = [user.id, user.name, user.score]  # TODO(kushal19057) | add error handling
    sheet.append_row(row)
    return {'data': user}

# references :
# https://fastapi.tiangolo.com/tutorial/
# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
# https://www.section.io/engineering-education/flask-crud-api/
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
# test endpoints using postman on localhost and deta
