from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)

    def __init__(self, username, password): 
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Commander = db.Column(db.String, nullable=False)
    Cards = db.Column(db.String, nullable=False)
    Views = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    def __init__(self, commander, cards, views=0): 
        self.commander = commander
        self.cards = cards
        self.views = views
        self.user_id = user_id

class DeckSchema(ma.Schema):
    class Meta:
        fields = ("id", "commander", "cards", "user_id")

deck_schema = DeckSchema()
multiple_deck_schema = DeckSchema(many=True)


@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data for add_user must be sent as json")
    
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_record = User(username, pw_hash)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(user_schema.dump(new_record))

@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))

@app.route("/user/get/<username>", methods=["GET"])
def get_user(username):
    user = db.session.query(User).filter(User.username == username).first()
    return jsonify(user_schema.dump(user))


@app.route("/user/verification", methods=["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("Error: Data for verification must be sent as json")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify("Unable to verify user credentials")

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify("Unable to verify user credentials")

    return jsonify(user_schema.dump(user))

@app.route("/deck/get", methods=["GET"])
def get_all_decks():
    all_decks = db.session.query(Deck).all()
    return jsonify(deck_schema.dump(Deck))

@app.route("/deck/update", methods=["PUT"])
def update_deck():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as json")

    views = request.json.get("views")
    commander = request.json.get("commander")
    cards = request.json.get("cards")
    deck = db.session.query(Deck).filter(Deck.id == id).first()

    deck.views = views
    deck.commander = commander
    deck.cards = cards
    db.session.commit()

    return jsonify(deck_schema.dump(deck))

@app.route("/deck/add", methods=["POST"])
def add_deck():
    if request.content_type != "application/json":
        return jsonify("Error: Data for add_deck must be sent as json")
    
    post_data = request.get_json()
    cards = post_data.get("cards")
    user_id = post_data.get("user_id")

    new_record = Deck(name, user_id)
    db.session.add(new_record)
    db.session.commit()

    deck = post_data

    return jsonify(deck_schema.dump(deck))
    

# YOU CAN CONVERT A DICTIONARY INTO JSON DO THAT FOR DECK LIST USING A SCHEMA.DUMP

if __name__ == "__main__":
    app.run(debug=True)