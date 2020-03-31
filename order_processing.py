import json
import sys
import os
import urllib.request
# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika


def receivePayment():
    hostname = "localhost" # default broker hostname
    port = 5672 # default port
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="order_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="payment", durable=True) # 'durable' makes the queue survive broker restarts
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='payment.info') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    # delete_cart(username)
    print("Payment Success")

# def processOrderError(order):
#     print("Processing an order error:")
#     print(order)

# def delete_cart(username):
#     urllib.request.urlopen('http://127.0.0.1:8005/cart/delete/'+ str(username))
#     if (urllib.request.urlopen(req)):
#         print("Deleted")

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": processing payment...")
    receivePayment()
