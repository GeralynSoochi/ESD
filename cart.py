from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


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
 
 
@app.route("/cart", methods=['GET'])
def get_all():
    return jsonify({"cart": [cart.json() for cart in Cart.query.all()]})

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


@app.route("/cart/delete", methods=["DELETE"])
def delete():
    data = request.get_json()

    username = data['username']
    name = data['name']
    description = data['description']
    price = data['price']
    imageLink = data['imageLink']

    remove_cart = Cart(username, name, description, price, imageLink)
    
    db.session.delete(remove_cart)
    db.session.commit()

    return jsonify({"message" : "success"}), 200

 
if __name__ == '__main__':
    app.run(port=5005, debug=True)