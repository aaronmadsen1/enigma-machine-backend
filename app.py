from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://oogdmqigyrfjax:da430207fb2b42dd7f17ed9535b4be6624d5f46cfef6bd3bd947d3a9f68dbc92@ec2-54-235-180-123.compute-1.amazonaws.com:5432/dc0igokc4vi99d"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Message(db.Model):
  __tablename__ = "messages"
  id = db.Column(db.Integer, primary_key=True)
  encryption = db.Column(db.Text)

  def __init__(self, encryption):
    self.encryption = encryption


class MessageSchema(ma.Schema):
  class Meta:
    fields = ("id", "encryption")

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

# * * * * * * * * * * * * * MAY NOT NEED * * * * * * * * * * * * * * * 
@app.route("/messages", methods=["GET"])
def get_messages():
  all_Messages = Message.query.all()
  result = messages_schema.dump(all_Messages)
  return jsonify(result)


@app.route("/message/<id>", methods=["GET"])
def get_message(id):
  message = Message.query.get(id)
  return message_schema.jsonify(message)


@app.route("/message", methods=["POST"])
def add_message():
  encryption = request.json["encryption"]

  new_message = Message(encryption)
  db.session.add(new_message)
  db.session.commit()

  created_message = Message.query.get(new_message.id)
  return message_schema.jsonify(created_message)


# * * * * * * * * * * * * * MAY NOT NEED * * * * * * * * * * * * * * * 
# @app.route("/message/<id>", methods=["PUT"])
# def update_message(id):
#   message = Message.query.get(id)
#   message.encryption = request.json["encryption"]

#   db.session.commit()
#   return message_schema.jsonify(message)


@app.route("/message/<id>", methods=["DELETE"])
def delete_message(id):
  message = Message.query.get(id)
  db.session.delete(message)
  db.session.commit()
  return "MESSAGE DELETED"


if __name__ == "__main__":
  app.debug = True
  app.run()