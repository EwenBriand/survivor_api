import requests
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
import bcrypt


client = pymongo.MongoClient(
    "mongodb+srv://hello:4SGDlVXcixYzsyKf@cluster0.2ndba1e.mongodb.net/")

db = client["survivor"]

private = db["workshop"]

data = list(private.find())

password = "password".encode('utf-8')
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(10))

private.update_many({}, {"$set": {"rgb": "#FFFFFF"}})

# pe = []

# for i in data:
#     temp = {
#         "id": i["id"],
#         "name": i["name"],
#         "surname": i["surname"]
#     }
#     pe.append(temp)

# url = "https://pds9gspmwy.eu-west-1.awsapprunner.com/api/chat/create_chan"

# payload = json.dumps({
#     "people_in": pe,
# })
# headers = {
#     'accept': 'application/json',
#     'X-Group-Authorization': 'XB9ELKZ0mpNUuiJsPimI_XbEZW8Wve7c',
#     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzQsImVtYWlsIjoib2xpdmVyLmxld2lzQG1hc3VyYW8uanAiLCJuYW1lIjoiT2xpdmVyIiwic3VybmFtZSI6Ikxld2lzIiwiZXhwIjoxNjk1NzIwMjgwfQ.bTSKDM0q_n1cIAhFHivWGYHUAnEOGTvgsniJTz4V-Ps',
#     'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)

#  NT
# while True:
#     url = "https://masurao.fr/api/employees/login"

#     payload = json.dumps({
#         "email": "oliver.lewis@masurao.jp",
#         "password": "password"
#     })
#     headers = {
#         'accept': 'application/json',
#         'X-Group-Authorization': 'a6c42607031f2cbcb2a43a9c109f8219',
#         'Content-Type': 'application/json'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)

#     print(response.text)
