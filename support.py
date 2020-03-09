import json
import sys
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import requests

class Book(db.Model):
    __tablename__ = 'book'

    isbn13 = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)

    def __init__(self, isbn13, title, price, availability):
        self.isbn13 = isbn13
        self.title = title
        self.price = price
        self.availability = availability

    def json(self):
        return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}


@app.route("/support", methods=['POST'])
def create_ticket(ticketid):
    if (Ticket.query.filter_by(ticketid=ticketid).first()):
        return jsonify({"message": "A ticket with ticketid '{}' already exists.".format(ticketid)}), 400

    data = request.get_json()
    ticket = Ticket(ticketid, **data)

    try:
        db.session.add(ticket)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the ticket."}), 500

    return jsonify(ticket.json()), 201


@app.route("/support/<int:ticketid>")
def retrieve_ticket(ticketid):
    ticket = Ticket.query.filter_by(ticketid=ticketid).first
    if ticket:
        return jsonify(ticket.json())
    return jsonify({"message": "Ticket not found."}), 404


if __name__ == '__main__':
    app.run(port=5010, debug=True)
