from flask import Flask, render_template, jsonify, request
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

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  # CHANGE THIS PART
  "client_id": "AQAo5U4GVQPwJ-pYrultYc5UsQXap7JI1eCjpfL2Bhy7mUau1hVY9BSEnOc3dIYOIFdAnu_C8bbciG2p",
  "client_secret": "EHU2C0gfNoFH6lLLknJsAYKyzlJ_oj_cYg7eg7uyuIn_qTn8CjVztWNgiJjh1_2X3qD-drZVMIKVoRca" })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment', methods=['POST'])
def payment():
    data = request.get_json()
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            # "item_list": {
            #     "items": [{
            #         "name": "testitem",
            #         "sku": "12345",
            #         "price": "500.00",
            #         "currency": "USD",
            #         "quantity": 1}]},
            "amount": {
                "total": data['total'],
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Login success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False
    
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
        send_noti()

    else:
        print(payment.error)

    return jsonify({'success' : success})

def send_noti():
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
    message = "Payment success"

    # send the message
    # always inform Monitoring for logging no matter if successful or not
    channel.basic_publish(exchange=exchangename, routing_key="payment.info", body=message)
        # By default, the message is "transient" within the broker;
        #  i.e., if the monitoring is offline or the broker cannot match the routing key for the message, the message is lost.
        # If need durability of a message, need to declare the queue in the sender (see sample code below).
    
    # inform Error handler
    channel.queue_declare(queue='payment', durable=True) # make sure the queue used by the error handler exist and durable
    channel.queue_bind(exchange=exchangename, queue='payment', routing_key='payment.info') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="payment.info", body=message,
        properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
    )
    print("Message sent.")
    connection.close()


if __name__ == '__main__':
    app.run(port=5008, debug=True)
