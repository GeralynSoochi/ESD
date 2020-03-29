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
telegramURL = "https://api.telegram.org/bot733055974:AAEsyKoq3z5mquv0k_xmzugu_dej_1MbdtA/sendMessage?chat_id=-1001267215209&parse_mode=Markdown&text="

@app.route("/CreateSupportTicket/", methods=['POST'])
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
        return jsonify({"message": "Your ticket has been logged, however there was an issue with the email service. You might not receive an email."}), 404

    #send telegram messages to support staff
    bot_message = "User " +  ticket["username"] + " submitted a new ticket. \nThe details are as follows:\nTicket ID: " + str(ticket["ticketid"]) + "\nIssue Title: " + ticket["issuetitle"] + "\nIssue Details: " + ticket["issuedetails"]
    send_text = telegramURL + bot_message
    response = requests.get(send_text)
    response = response.json()
    if response["ok"] == False:
        return jsonify({"message": "Your ticket has been logged. We apologise in advance for any delays in support replies."}), 404

    return jsonify(ticket), 201


if __name__ == '__main__':
    app.run(port=5010, debug=True)