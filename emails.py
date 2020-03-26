import json
import sys
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from mailjet_rest import Client

app = Flask(__name__)

CORS(app)

@app.route("/emails/", methods=['POST'])
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
  
  content = {
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
  print(content)
  result = mailjet.send.create(data=content)
  print (result.status_code)
  print (result.json())
  return result.json(), result.status_code

if __name__ == '__main__':
    app.run(port=5012, debug=True)