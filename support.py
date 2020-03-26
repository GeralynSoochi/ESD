import json
import sys
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
CORS(app)

import requests
ticketURL = "http://localhost:5011/ticket/"
accountURL = "http://localhost:5003/account/"
emailsURL = "http://localhost:5012/emails/"


@app.route("/support/", methods=['POST'])
def send_ticket():
    data = request.get_json()

    #get user details: account.py
    r = requests.get(accountURL + data["username"], timeout=2)
    result = json.loads(r.text.lower())
    if r.status_code != requests.codes.ok: #return error message
        return jsonify({"message": "Your username is invalid. Please check your login details."}), 404
    print(result)

    #create ticket: ticket.py
    r = requests.post(ticketURL, json = data)
    ticket = json.loads(r.text.lower())
    if r.status_code != 201: #return error message
        return jsonify({"message": "An error occurred creating the ticket. Please check your ticket details."}), 500


    #send email: emails.py
    ticketdetails = {"ticketid": ticket["ticketid"], "dateOpen": ticket["dateopen"], "issueTitle": ticket["issuetitle"], "issueDetails": ticket["issuedetails"], "username": ticket["username"], "email": result["email"]}
    r = requests.post(emailsURL, json = ticketdetails)
    if r.status_code != requests.codes.ok: #return error message
        return jsonify({"message": "Your ticket has been logged, however there was an issue with the email service."}), 404

    return jsonify(ticket), 201


if __name__ == '__main__':
    app.run(port=5010, debug=True)