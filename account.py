from authy.api import AuthyApiClient
from flask_sqlalchemy import SQLAlchemy
from flask import Flask , request , render_template, redirect, url_for , session, Response , jsonify, json
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config.from.object('config')
api = AuthyApiClient('RpvEtSmOuQHVfDYe2UkRj50ustyfT028')
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


@app.route("/signup", methods =["POST"])
def signup():
        data = request.json
        phoneNumber =data
       
        #session['phoneNumber'] = phoneNumber
        #test = session.get
        api.phones.verification_start(phoneNumber , "+65" , via="sms")
        
        return jsonify({"message": "success"}), 200
        #data = {'message': 'Created', 'code': 'SUCCESS'}
        #return make_response(jsonify(data), 200)

        #return json.dumps({'phoneNumber':phoneNumber}), 200, {'ContentType':'application/json'}

        #return redirect("http://localhost/git-esd/ESD/verifyaccount")

        #return redirect(url_for("http://localhost/git-esd/ESD/verifyaccount"))


@app.route("/verifyaccount", methods =["GET", "POST"])
def verifyaccount():
        #if request.method == "POST":
        #token = request.form.get("token")
        data = request.json
        #phoneNumber = session.get('phoneNumber')
        
        token = data['token']
        phoneNumber = data['phoneNumber']
        

        verification = api.phones.verification_check(phoneNumber, "+65" , token)
        if verification.ok():
            username = data['fullName'] 
            email = data['email']
            password = data['password']
            if (Account.query.filter_by(phone=phoneNumber).first()):
                return jsonify({"message": "An account with  " + phoneNumber + "already exists."}), 400
            newAccount = Account(username, password,email,phoneNumber)
            #test = 0
            try:
                db.session.add(newAccount)
                db.session.commit()
                #test = newAccount.id
            except:
                return jsonify({"message": "An error occurred creating the account."}), 500    
            return jsonify({"message" : "success", "username" : username}), 200
            
        else:
                return jsonify({"message": "message dont work"}), 400


    #return render_template("verifyaccount.html")

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
