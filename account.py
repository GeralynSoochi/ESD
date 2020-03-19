import json
import sys
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/account'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

import requests

class Account(db.Model):
    __tablename__ = 'account'
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False)


    def __init__(self, username, password, email, phone):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone


    def json(self):
        return {"username": self.username, "password": self.password, "email": self.email, "phone": self.phone}

@app.route("/account")
def get_all():
    return jsonify({"account": [account.json() for account in Account.query.all()]})

@app.route("/account/<string:username>")
def login(username):
    account = Account.query.filter_by(username=username).first()
    if account:
        return jsonify(account.json())
    return jsonify({"message": "User not found."}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
