import telecomchatbot as chatbot
from __init__ import create_app

# Flask
from flask import Flask, request, jsonify, json, render_template
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import datetime
import json
import os
from dotenv import load_dotenv

from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

from utils import write_message, get_user_messages
# from auth import authentication
import auth
authentication = auth.authentication


load_dotenv()

app = create_app()
# app = Flask(__name__)

CORS(app)

app.register_blueprint(authentication, url_prefix="/api/auth")

# mail_settings = {
#     "MAIL_SERVER": 'smtp.gmail.com',
#     "MAIL_PORT": 465,
#     "MAIL_USE_TLS": False,
#     "MAIL_USE_SSL": True,
#     "MAIL_USERNAME": os.getenv('EMAIL_USER'),
#     "MAIL_PASSWORD": os.getenv('EMAIL_PASSWORD')
# }

# app.config.update(mail_settings)

# mail = Mail(app)

#GET /, test route
@app.route('/', methods=["GET"])
def testGet():
    return jsonify({"userId": 1,"isBot": True}), 200

# POST /telecom
@app.route('/telecom', methods=["POST"])
def chatbotReply():
    # context = chatbot.context
    message = request.get_json()
    id = message['id']
    messageText = message['message']
    userId = message['userId']
    context = message['context']
    #write user message to database
    write_message(id, userId, messageText, False, datetime.datetime.now())
    reply, context = chatbot.response(messageText, userId, context)
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    ident = json.dumps(datetime.datetime.utcnow(), default=date_handler).strip('"')
    #write chatbot reply to database
    write_message(ident, userId, reply, True, datetime.datetime.now())
    return jsonify({"userId": userId, "id": ident, "message": reply, "isBot": True, "context": context}), 200
    
@app.route('/telecom/messages/<user_id>', methods=["GET"])
def getMessages(user_id):
    print(jsonify(get_user_messages(user_id)))
    return jsonify(get_user_messages(user_id)), 200





app.run(port=5000, debug=True)