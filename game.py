from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/game'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
CORS(app)
 
 
class Game(db.Model):
    __tablename__ = 'game'
 
    id = db.Column(db.String(13), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    price = db.Column(db.Float(precision=2))
    category = db.Column(db.String(100))
    imageLink = db.Column(db.String(100))
 
    def __init__(self, id, name, description, price, category, imageLink):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.imageLink = imageLink
 
    def json(self):
        return {"id": self.id, "name": self.name, "description": self.description, "price": self.price, "category": self.category, "imageLink": self.imageLink}
 
 
@app.route("/game")
def get_all():
    return jsonify({"games": [game.json() for game in Game.query.all()]})
 
 
@app.route("/game/<string:id>", methods = ['GET'])
def find_by_id(id):
    game = Game.query.filter_by(id=id).first()
    if game:
        return jsonify(game.json())
    return jsonify({"message": "Game not found."}), 404

if __name__ == '__main__':
    # app.run(port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)