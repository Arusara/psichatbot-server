# Flask
from flask import Flask, request, jsonify, json, render_template
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import os
from dotenv import load_dotenv

load_dotenv()

mail = Mail()

def create_app():
    app = Flask(__name__)
    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": os.getenv('EMAIL_USER'),
        "MAIL_PASSWORD": os.getenv('EMAIL_PASSWORD')
    }

    app.config.update(mail_settings)

    mail.init_app(app)

    return app
