import json
import sys
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ticket'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

import requests

class Ticket(db.Model):
    __tablename__ = 'ticket'

    ticketid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    issueTitle = db.Column(db.String(100), nullable=False)
    issueDetails = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    dateOpen = db.Column(db.DateTime(), nullable=False)
    username = db.Column(db.String(100), nullable=False)

    def __init__(self, dateOpen, issueTitle, issueDetails, status, username):
        self.dateOpen = dateOpen
        self.issueTitle = issueTitle
        self.issueDetails = issueDetails
        self.status = status
        self.username = username

    def json(self):
        return {"ticketid": self.ticketid, "dateOpen": self.dateOpen, "issueTitle": self.issueTitle, "issueDetails": self.issueDetails, "status": self.status, "username": self.username}

@app.route("/ticket/", methods=['POST'])
def create_ticket():

    data = request.get_json()
    dateOpen = date.today()
    ticket = Ticket(dateOpen = dateOpen, issueTitle = data["issueTitle"], issueDetails = data["issueDetails"], status = data["status"], username = data["username"])

    try:
        db.session.add(ticket)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the ticket."}), 500
    ticket = Ticket.query.filter_by(ticketid=ticket.ticketid).first()
    print(ticket.ticketid)
    return jsonify(ticket.json()), 201


@app.route("/ticket/<int:ticketid>")
def retrieve_ticket(ticketid):
    ticket = Ticket.query.filter_by(ticketid=ticketid).first()
    if ticket:
        return jsonify(ticket.json())
    return jsonify({"message": "Ticket not found."}), 404

@app.route("/ticket/get/<string:username>")
def retrieve_tickets(username):
    print(jsonify({"tickets": [ticket.json() for ticket in Ticket.query.filter_by(username=username).all()]}))
    return jsonify({"tickets": [ticket.json() for ticket in Ticket.query.filter_by(username=username).all()]})


if __name__ == '__main__':
    app.run(port=5011, debug=True)