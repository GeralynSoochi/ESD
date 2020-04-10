from authy.api import AuthyApiClient
from flask_sqlalchemy import SQLAlchemy
from flask import Flask , request , render_template, redirect, url_for , session, Response , jsonify, json
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/account'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = AuthyApiClient('4tYKyCOlMme0A0nXpqk2hoK68TOdBies')
app.secret_key = 'Foobarj823!42vs#46Jd_d3_Zaylk@'
app.config.from_object(__name__)
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


@app.route("/signup/<string:username>", methods =["POST"])
def signup(username):
        data = request.json
        username = data['username']
        password = data['password']
        email = data['email']
        phone = data['phoneNumber']
        if (Account.query.filter_by(username=username).first()):
            return jsonify({"message": "An account with username '{}' already exists.".format(username)}), 400
        elif (Account.query.filter_by(email=email).first()):
            return jsonify({"message": "An account with email '{}' already exists.".format(email)}), 400
        elif (Account.query.filter_by(phone=phone).first()):
            return jsonify({"message": "An account with phone '{}' already exists.".format(phone)}), 400
        try:
            api.phones.verification_start(phone , "+65" , via="sms")
            account = Account(username, password, email,phone)
            print("success")
        except:
            print("fail")
            return jsonify({"message": "An error occurred sending the OTP. Please try again later"}), 500
        return jsonify(account.json()), 201

@app.route("/fb/<string:username>", methods =["POST"])
def fb(username):
        data = request.json
        username = data['username']
        password = data['password']
        email = data['email']
        phone = data['phoneNumber'] 
        newaccount = Account(username, password, email,phone)
        try:
            print("here")
            db.session.add(newaccount)
            print("here2")
            db.session.commit()
            print("here3")
            return jsonify({"message": "success"}), 200
        except:
            return jsonify({"message": "An error occurred creating the account."}), 500    

@app.route("/verifyaccount", methods =["POST"])
def verifyaccount():
        data = request.json
        token = data['token']
        phoneNumber = data['phoneNumber']
        

        verification = api.phones.verification_check(phoneNumber, "+65" , token)
        

        if verification.ok():
            username = data['username'] 
            email = data['email']
            password = data['password']
            newAccount = Account(username, password,email,phoneNumber)
            try:
                db.session.add(newAccount)
                db.session.commit()
                return jsonify({"message": "success"}), 200
            except:
                return jsonify({"message": "An error occurred creating the account."}), 500    
            
        else:
            return jsonify({"message": "otp is wrong"}), 400


@app.route("/account/<string:username>")
def login(username):
    account = Account.query.filter_by(username=username).first()
    if account:
        return jsonify(account.json())
    return jsonify({"message": "User not found."}), 404

if __name__ == '__main__':
   app.run(port=5003, debug=True)
