import telecomchatbot as chatbot

# Flask
from flask import Flask, request, jsonify, json
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import datetime
import json
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

# from auth import authentication
import auth
authentication = auth.authentication

app = Flask(__name__)

CORS(app)

app.register_blueprint(authentication, url_prefix="/api/auth")

#GET /, test route
@app.route('/', methods=["GET"])
def testGet():
    return jsonify({"userId": 1,"isBot": True}), 200

# POST /telecom
@app.route('/telecom', methods=["POST"])
def chatbotReply():
    # context = chatbot.context
    message = request.get_json()
    messageText = message['message']
    userId = message['userId']
    context = message['context']
    # if not userId in context.keys():
    #     chatbot.context[userId]=""
    # while userId not in context.keys():
    #     pass
    reply, context = chatbot.response(messageText, userId, context)
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    ident = json.dumps(datetime.datetime.now(), default=date_handler).strip('"')
    return jsonify({"userId": 1, "id": ident, "message": reply, "isBot": True, "context": context}), 200
    

#app.run(port=5000, debug=True)