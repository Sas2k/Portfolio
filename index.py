from flask import Flask, render_template, request
from random import randint

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_key'] = f'{os.urandom(randint(20, 50))}'

uri = f"mongodb+srv://sas2k:{os.getenv('DBPass')}@clientbase.pk701wj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
clients = []

db = client.Clients
cluster = db.Data

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        items = {
            'Name': data['UserName'],
            'Email': data['UserEmail'],
            'Message': data['TextBody']
        }
        cluster.insert_one(items)
        print(cluster.find_one())
    return render_template('index.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)