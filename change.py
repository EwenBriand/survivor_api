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

with open('db_survivor.json', 'r') as f:
    data = json.load(f)

print(data[1]["id"])

for i in range(len(data)):
    print(i)
    data[i]["url"] = "https://mysurvivor.s3.amazonaws.com/img/" + \
        str(data[i]["id"]) + ".png"

with open('db_survivor.json', 'w') as f:
    json.dump(data, f)
