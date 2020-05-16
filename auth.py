from flask import Blueprint, request, Response, jsonify
from flask_cors import CORS, cross_origin
import datetime
from utils import validate_user_input, generate_salt, generate_hash, db_write, validate_user

authentication = Blueprint("authentication", __name__)


@authentication.route("/register", methods=["POST"])
def register_user():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    user_email = request.json["email"]
    user_password = request.json["password"]
    created = datetime.datetime.now()
    # user_confirm_password = request.json["confirm_password"]

    if validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)

        if db_write(
            """INSERT INTO users (email, first_name, last_name, password_salt, password_hash, created) VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_email, first_name, last_name, password_salt, password_hash, created),
        ):
            print("Registered" + user_email)
            return Response(status=201)
        else:
            return Response(status=409)
    else:
        return Response(status=400)


@authentication.route("/login", methods=["POST"])
def login_user():
    print(request.json)
    user_email = request.json["email"]
    user_password = request.json["password"]

    user_token, error_string = validate_user(user_email, user_password)

    if user_token:
        print(user_token)
        return jsonify({"jwt_token": user_token, "message": "Successfully logged in: " + user_email})
    else:
        if error_string=="email":
            return jsonify({"error": "email"}), 401

        elif error_string=="password":
            return jsonify({"error": "password"}), 401

    
