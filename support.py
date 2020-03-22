import json
import sys
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from mailjet import sendemail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ticket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

import requests
accountURL = "http://localhost:5000/account/"

class Ticket(db.Model):
    __tablename__ = 'ticket'

    ticketid = db.Column(db.Integer, primary_key=True)
    issueTitle = db.Column(db.String(100), nullable=False)
    issueDetails = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    dateOpen = db.Column(db.DateTime(), nullable=False)
    username = db.Column(db.String(100), nullable=False)

    def __init__(self, ticketid, dateOpen, issueTitle, issueDetails, status, username):
        self.ticketid = ticketid
        self.dateOpen = dateOpen
        self.issueTitle = issueTitle
        self.issueDetails = issueDetails
        self.status = status
        self.username = username

    def json(self):
        return {"ticketid": self.ticketid, "dateOpen": self.dateOpen, "issueTitle": self.issueTitle, "issueDetails": self.issueDetails, "status": self.status, "username": self.username}


@app.route("/support/<int:ticketid>", methods=['POST'])
def create_ticket(ticketid):
    if (Ticket.query.filter_by(ticketid=ticketid).first()):
        return jsonify({"message": "A ticket with ticketid '{}' already exists.".format(ticketid)}), 400

    data = request.get_json()
    dateOpen = date.today()
    ticket = Ticket(ticketid, dateOpen, **data)

    try:
        db.session.add(ticket)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the ticket."}), 500
    
    #get user details
    r = requests.get(accountURL + ticket.username, timeout=2)
    print(r)
    result = json.loads(r.text.lower())
    print(result)

    sendemail(ticket.ticketid, ticket.dateOpen, ticket.issueTitle, ticket.issueDetails, ticket.username, result["email"])
    return jsonify(ticket.json()), 201


@app.route("/support/<int:ticketid>")
def retrieve_ticket(ticketid):
    ticket = Ticket.query.filter_by(ticketid=ticketid).first()
    if ticket:
        return jsonify(ticket.json())
    return jsonify({"message": "Ticket not found."}), 404


if __name__ == '__main__':
    app.run(port=5010, debug=True)
