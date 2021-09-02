from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)
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


@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data for add_user must be sent as json")
    
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    new_record = User(username, password)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(user_schema.dump(new_record))



if __name__ == "__main__":
    app.run(debug=True)