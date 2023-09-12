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

users = db["users"]
wdg = db["workshop"]

data = list(users.find())

for i in data:
    del i["_id"]

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

    return data, 200


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
        "subordinates": [],
        "url": "https://mysurvivor.s3.amazonaws.com/img/74.png"
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


@app.route('/api/chat/all_by_names', methods=['POST'])
def get_all_by_name():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()
    id_list = data2["ids"]

    for i in range(len(id_list)):
        id_list[i] = int(id_list[i])

    response = list(private.find(
        {'people_in': {'$all': [{'$elemMatch': {'id': {'$in': id_list}}}]}}))

    if response is None:
        return 'Not found', 404

    i = 0
    while i != len(response):
        count = 0
        for j in range(len(response[i]["people_in"])):
            if response[i]["people_in"][j]["id"] in id_list:
                count += 1
        if count == len(id_list):
            response[i]["_id"] = str(response[i]["_id"])
        else:
            del response[i]
            i -= 1
        i += 1

    return response, 200


@app.route('/api/chat/send_ms', methods=['POST'])
def send_ms():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()

    if data2 is None or "id_chan" not in data2 or "id" not in data2 or "text" not in data2:
        return 'Bad body', 400

    id_ms = len(private.find_one(
        {"_id": ObjectId(data2["id_chan"])})["all_messages"])

    private.update_one({"_id": ObjectId(data2["id_chan"])}, {"$push": {"all_messages": {"id_ms": id_ms, "id": int(
        data2["id"]), "content": data2["text"], "date": datetime.now().strftime('%d:%m:%Y'), "hours": datetime.now().strftime('%H:%M')}}})

    return "ok", 200


@app.route('/api/chat/create_chan', methods=['POST'])
def create_chan():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()

    if data2 is None or "people_in" not in data2:
        return 'Bad body', 400

    for i in range(len(data2["people_in"])):
        data2["people_in"][i]["id"] = int(data2["people_in"][i]["id"])

    result = private.insert_one(
        {"people_in": data2["people_in"], "all_messages": []})
    inserted_id = str(result.inserted_id)
    return inserted_id, 200


@app.route('/api/chat/private_chan', methods=['GET'])
def private_chan():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    id = request.args.get('id1')
    id2 = request.args.get('id2')
    print("id: ", id, id2)
    response = private.find_one({'people_in': {'$size': 2, '$all': [
                                {'$elemMatch': {'id': int(id)}}, {'$elemMatch': {'id': int(id2)}}]}})
    print(response)

    if response is None:
        return 'Not found', 404

    response["_id"] = str(response["_id"])
    return response, 200


@app.route('/api/chat/find_by_id', methods=['GET'])
def find_by_id():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    id = request.args.get('id')
    print("id: ", id)
    if id == "0":
        return 'Bad request', 400
    response = private.find_one({'_id': ObjectId(id)})

    if response is None:
        return 'Not found', 404

    response["_id"] = str(response["_id"])
    return response, 200


@app.route('/api/chat/modify_ms', methods=['POST'])
def modify_ms():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()

    if data2 is None or "id_chan" not in data2 or "id_ms" not in data2 or "text" not in data2:
        return 'Bad body', 400

    query = {"_id": ObjectId(data2["id_chan"]), "all_messages": {
        '$elemMatch': {'id_ms': data2["id_ms"]}}}
    update = {"$set": {"all_messages.$.content": data2["text"], "all_messages.$.date": datetime.now(
    ).strftime('%d:%m:%Y'), "all_messages.$.hours": datetime.now().strftime('%H:%M')}}
    private.update_one(query, update)
    # private.update_one({"_id": ObjectId(data2["id_chan"]), "all_messages": {'$all': [{'$elemMatch': {'id_ms': data2["id_ms"]}}]}}, {{"all_messages": {"content": data2["text"], "date": datetime.now().strftime('%d:%m:%Y'), "hours": datetime.now().strftime('%H:%M')}}})

    return "ok", 200


@app.route('/api/wdg/create', methods=['POST'])
def create_wdg():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()

    if data2 is None or "name" not in data2 or "url" not in data2 or "urlImage" not in data2:
        return 'Bad body', 400

    result = wdg.insert_one(
        {"name": data2["name"], "url": data2["url"], "urlImage": data2["urlImage"]})

    return str(result.inserted_id), 200


@app.route('/api/wdg/get_by_id', methods=['GET'])
def get_wdg_by_id():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    id = request.args.get('id')

    if id == None or id == "0" or id == "":
        return 'Bad request', 400

    response = wdg.find_one({'_id': ObjectId(id)})
    if response is None:
        return 'Not found', 404

    response["_id"] = str(response["_id"])
    return response, 200


@app.route('/api/wdg/get_all', methods=['GET'])
def get_all_wdg():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    response = list(wdg.find())
    if response is None:
        return 'Not found', 404

    for i in range(len(response)):
        response[i]["_id"] = str(response[i]["_id"])

    return response, 200


@app.route('/api/wdg/add_wdg_to_emp', methods=['POST'])
def add_wdg_to_emp():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()

    if data2 is None or "id_emp" not in data2 or "id_wdg" not in data2:
        return 'Bad body', 400

    users.update_one({"id": int(data2["id_emp"])}, {
                     "$addToSet": {"widgets": ObjectId(data2["id_wdg"])}})
    return "ok", 200


@app.route('/api/wdg/rm_wdg_to_emp', methods=['POST'])
def rm_wdg_to_emp():
    if check_aut2(request) != True or check_aut(request) != True:
        return 'Bad Aut', 400
    data2 = request.get_json()

    if data2 is None or "id_emp" not in data2 or "id_wdg" not in data2:
        return 'Bad body', 400

    users.update_one({"id": int(data2["id_emp"])}, {
                     "$pull": {"widgets": ObjectId(data2["id_wdg"])}})
    return "ok", 200


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
    # app.run(debug=True)

#  http://127.0.0.1:5000
