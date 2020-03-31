from flask import Flask, render_template, jsonify, request
import paypalrestsdk

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
        print('Payment success!')
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
        #amqp to cart
    else:
        print(payment.error)

    return jsonify({'success' : success})

if __name__ == '__main__':
    app.run(port=5008, debug=True)