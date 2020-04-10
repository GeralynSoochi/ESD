from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import paypalrestsdk

import json
import sys
import os
import random
import datetime
import urllib.request

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
# Use a reply-to queue and correlation_id to get a corresponding reply
import pika

hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="cart_direct"
channel.exchange_declare(exchange=exchangename, exchange_type='direct')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
CORS(app)




class Cart(db.Model):
    __tablename__ = 'cart'
 
    username = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), primary_key=True)
    description = db.Column(db.String(500))
    price = db.Column(db.Float(precision=2))
    imageLink = db.Column(db.String(100))
 
    def __init__(self, username, name, description, price, imageLink):
        self.username = username
        self.name = name
        self.description = description
        self.price = price
        self.imageLink = imageLink
 
    def json(self):
        return {"username": self.username, "name": self.name, "description": self.description, "price": self.price, "imageLink": self.imageLink}
 

@app.route("/cart/<string:username>", methods=['GET'])
def get_all(username):
    return jsonify({"cart": [cart.json() for cart in Cart.query.filter_by(username = username)]})

@app.route("/cart", methods=['POST'])
def create_cart():

    data = request.get_json()

    username = data['username']
    name = data['name']
    description = data['description']
    price = data['price']
    imageLink = data['imageLink']

    new_cart = Cart(username, name, description, price, imageLink)

    db.session.add(new_cart)
    db.session.commit()
    return jsonify({"message" : "success"}), 200


@app.route("/cart/<string:username>/<string:name>", methods=["DELETE"])
def delete(username, name):
    remove_cart = Cart.query.filter_by(username = username, name = name).first()
    db.session.delete(remove_cart)
    db.session.commit()

    return jsonify({"message" : "success"}), 200

@app.route("/cart/delete/<string:username>", methods=["DELETE"])
def delete_by_user(username):
    remove_cart = Cart.query.filter_by(username = username).all()
    for item in remove_cart:
        db.session.delete(item)
        db.session.commit()

    return jsonify({"message" : "success"}), 200

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  # CHANGE THIS PART
  "client_id": "AQAo5U4GVQPwJ-pYrultYc5UsQXap7JI1eCjpfL2Bhy7mUau1hVY9BSEnOc3dIYOIFdAnu_C8bbciG2p",
  "client_secret": "EHU2C0gfNoFH6lLLknJsAYKyzlJ_oj_cYg7eg7uyuIn_qTn8CjVztWNgiJjh1_2X3qD-drZVMIKVoRca" })

@app.route('/payment', methods=['POST'])
def payment():
    data = request.get_json()
    print(data)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "amount": {
                "total": data['total'],
                "currency": "SGD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Login success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False
    data = request.get_json()
    username = request.form['user']
    amt = request.form['amt']
    
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
        send_noti(username, amt)

    else:
        print(payment.error)

    return jsonify({'success' : success})

def send_noti(user, amt):
    # default username / password to the borker are both 'guest'
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="order_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    message = user + " has paid $" + str(amt)

    # send the message
    channel.queue_declare(queue='payment', durable=True) # make sure the queue used by the error handler exist and durable
    channel.queue_bind(exchange=exchangename, queue='payment', routing_key='payment.info') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="payment.info", body=message,
        properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
    )
    print("Message sent.")
    connection.close()

 
if __name__ == '__main__':
    app.run(port=5005, debug=True)
