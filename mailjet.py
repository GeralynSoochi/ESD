import json
import sys
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from mailjet_rest import Client
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ticket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

@app.route("/email/", methods=['POST'])
# def sendemail(ticketid, dateOpen, issueTitle, issueDetails, username, email):
def sendemail():
  api_key = '8a1c7c18d061725a36de6e19d9f4a2f9'
  api_secret = 'fc8a89742489e2d8846eae8f750864d3'
  mailjet = Client(auth=(api_key, api_secret), version='v3.1')
  data = request.get_json()
  ticketid = data["ticketid"]
  dateOpen = data["dateOpen"]
  issueTitle = data["issueTitle"]
  issueDetails = data["issueDetails"]
  username = data["username"]
  email = data["email"]
  
  email = {
    'Messages': [
      {
        "From": {
          "Email": "scgoh.2018@sis.smu.edu.sg",
          "Name": "Geralyn"
        },
        "To": [
          {
            "Email": email,
            "Name": username
          }
        ],
        "Subject": "You opened a ticket.",
        "TextPart": "Here is your ticket",
        "HTMLPart": "Your ticket details are as follows: <br> Title: " + issueTitle + "<br> TicketID: " + str(ticketid) + "<br> Description: " + issueDetails + "<br> Date Opened: " + str(dateOpen),
        "CustomID": "AppGettingStartedTest"
      }
    ]
  }
  result = mailjet.send.create(data=email)
  print (result.status_code)
  print (result.json())
  print ("email")
  return result.json(), result.status_code

if __name__ == '__main__':
    app.run(port=5012, debug=True)