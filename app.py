import os
from flask import Flask, request, send_file, render_template
# import python as back
from flask_cors import CORS
import sys
import asyncio
from waitress import serve
import json
import pymongo
from bson.objectid import ObjectId
from datetime import datetime

client = pymongo.MongoClient(
    "mongodb+srv://Garry:MgA2kGlMI2PNkR90@cluster0.jbale6t.mongodb.net/test")

db = client["survivor"]

private = db["chatPrivate"]

with open('db_survivor.json', 'r') as f:
    data = json.load(f)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def check_aut(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header == 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzQsImVtYWlsIjoib2xpdmVyLmxld2lzQG1hc3VyYW8uanAiLCJuYW1lIjoiT2xpdmVyIiwic3VybmFtZSI6Ikxld2lzIiwiZXhwIjoxNjk1NzIwMjgwfQ.bTSKDM0q_n1cIAhFHivWGYHUAnEOGTvgsniJTz4V-Ps':
        return True
    return False


def check_aut2(request):
    authx_header = request.headers.get('X-Group-Authorization')
    if authx_header and authx_header == "XB9ELKZ0mpNUuiJsPimI_XbEZW8Wve7c":
        return True
    return False


@app.route('/api/employees', methods=['GET'])
def emp():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    response = []
    for i in data:
        if "id" in i:
            response.append({
                "id": i["id"],
                "email": i["email"],
                "name": i["name"],
                "surname": i["surname"]
            })
    return response, 200


@app.route('/api/employees/login', methods=['POST'])
def login():
    if check_aut2(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()
    if data2 is not None:
        if "email" in data2 and data2["email"] == "oliver.lewis@masurao.jp" and "password" in data2 and data2["password"] == "password":
            return {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzQsImVtYWlsIjoib2xpdmVyLmxld2lzQG1hc3VyYW8uanAiLCJuYW1lIjoiT2xpdmVyIiwic3VybmFtZSI6Ikxld2lzIiwiZXhwIjoxNjk1NzIwMjgwfQ.bTSKDM0q_n1cIAhFHivWGYHUAnEOGTvgsniJTz4V-Ps"
            }, 200
        else:
            return 'Bad body', 400
    else:
        return 'no body', 400


@app.route('/api/employees/me', methods=['GET'])
def me():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    return {
        "id": 74,
        "email": "oliver.lewis@masurao.jp",
        "name": "Oliver",
        "surname": "Lewis",
        "birth_date": "2000-08-13",
        "gender": "Male",
        "work": "Administrative Intern",
        "subordinates": []
    }, 200


@app.route('/api/employees/leader', methods=['GET'])
def leader():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    return [
        {
            "id": 1,
            "email": "billy.bob@masurao.jp",
            "name": "Billy",
            "surname": "Bob"
        }
    ], 200


@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_emp(employee_id):
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    id = int(employee_id)
    print("employee_id is", id)
    for i in data:
        if i["id"] == id:
            del i["_id"]
            return i, 200
    return 'Bad request', 400


@app.route('/api/employees/<int:employee_id>/image', methods=['GET'])
def get_img(employee_id):
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    id = int(employee_id)
    print("employee_id is", id)
    path = "./img/" + str(id) + ".png"

    if os.path.exists(path):
        return send_file(path, mimetype='image/png'), 200
    else:
        return 'Bad request', 400






@app.route('/api/chat/all_by_name', methods=['GET'])
def get_all_by_name():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    name = request.args.get('id')
    response = private.find({'people_in': {"id": int(name)}})
    print(response)

    return response, 200

@app.route('/api/chat/send_ms', methods=['POST'])
def send_ms():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()
    
    if data2 is None or "id_chan" not in data2 or "id" not in data2 or "text" not in data2:
        return 'Bad body', 400
    
    id_ms = len(private.find({"_id": ObjectId(data2["id_chan"])})["all_messages"])

    private.update_one({"_id": ObjectId(data2["id_chan"])}, {"$push": {"all_messages": {"id_ms": id_ms, "id": int(
        data2["id"]), "content": data2["text"], "date": datetime.now().strftime('%d:%m:%Y'), "hours": datetime.now().strftime('%H:%M')}}})
    
    return "ok", 200



if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
    # app.run(debug=True)

#  http://127.0.0.1:5000
