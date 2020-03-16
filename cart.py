from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
CORS(app)
 
 
class Game(db.Model):
    __tablename__ = 'cart'
 
    id = db.Column(db.String(13), primary_key=True)
    account = db.Column(db.String(13))
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    price = db.Column(db.Float(precision=2))
    category = db.Column(db.String(100))
    imageLink = db.Column(db.String(100))
 
    def __init__(self, account, name, description, price, category, imageLink):
        self.account = account
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.imageLink = imageLink
 
    def json(self):
        return {"account": self.account, "name": self.name, "description": self.description, "price": self.price, "category": self.category, "imageLink": self.imageLink}
 
 
@app.route("/game")
def get_all():
    return jsonify({"games": [game.json() for game in Game.query.all()]})
 
 
 
if __name__ == '__main__':
    app.run(port=5000, debug=True)