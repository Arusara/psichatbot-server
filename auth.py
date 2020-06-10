from flask import Blueprint, request, Response, jsonify, render_template
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
from random import randint
import datetime
from utils import validate_user_input, generate_salt, generate_hash, db_write, validate_user, \
    validate_user_registration_email, validate_user_registration_phone,\
    validate_user_update_email, validate_user_update_phone, check_if_verified,\
    check_verification_code, send_verification_email, get_verification_code

authentication = Blueprint("authentication", __name__)


@authentication.route("/register", methods=["POST"])
def register_user():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    user_email = request.json["email"]
    user_password = request.json["password"]
    user_phone_number = request.json["phone_number"]
    created = datetime.datetime.now()
    # user_confirm_password = request.json["confirm_password"]

    if validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)
        email_valid = validate_user_registration_email(user_email)
        phone_number_valid = validate_user_registration_phone(user_phone_number)
        verification_code = randint(10000, 99999)
        if email_valid and phone_number_valid:
            if db_write(
                """INSERT INTO users (email, phone_number, first_name, last_name, password_salt, password_hash, created, verification_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (user_email, user_phone_number, first_name, last_name, password_salt, password_hash, created, verification_code),
            ):
                print("Registered: " + user_email)
                send_verification_email(user_email, first_name, verification_code)
                return Response(status=200)
            else:
                return Response(status=409)
        else:
            err = ""
            if not email_valid:
                err += "email"
            if not phone_number_valid:
                err += "phone"
            return jsonify({"error": err}), 401
    else:
        return Response(status=400)


@authentication.route("/login", methods=["POST"])
def login_user():
    print(request.json)
    user_email = request.json["email"]
    user_password = request.json["password"]

    user_token, error_string, verified = validate_user(user_email, user_password)

    if user_token and verified:
        print(user_token)
        return jsonify({"jwt_token": user_token, "message": "Successfully logged in: " + user_email})
    elif user_token and not verified:
        print ("not verified")
        return jsonify({"verification_token": user_token, "error": "verification"}), 401
    else:
        if error_string=="email":
            return jsonify({"error": "email"}), 401

        elif error_string=="password":
            return jsonify({"error": "password"}), 401


@authentication.route("/update", methods=["POST"])
def update_user():
    user_id = request.json["user_id"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    user_email = request.json["email"]
    user_password = request.json["password"]
    user_phone_number = request.json["phone_number"]

    if validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)
        email_valid = validate_user_update_email(user_email, user_id)
        phone_number_valid = validate_user_update_phone(user_phone_number, user_id)
        if email_valid and phone_number_valid:
            if db_write(
                """UPDATE users SET email =%s, phone_number =%s, first_name =%s, last_name =%s, password_salt =%s, password_hash =%s WHERE user_id = %s""",
                (user_email, user_phone_number, first_name, last_name, password_salt, password_hash, user_id),
            ):
                print("Updated: " + user_email)
                return Response(status=200)
            else:
                return Response(status=409)
        else:
            err = ""
            if not email_valid:
                err += "email"
            if not phone_number_valid:
                err += "phone"
            return jsonify({"error": err}), 401
    else:
        return Response(status=400)

@authentication.route("/verify", methods=["POST"])
def verify_user():
    print(request.json)
    user_email = request.json["email"]
    verification_code = request.json["verification"]

    verified = check_if_verified(user_email)
    if not verified:
        if check_verification_code(user_email, verification_code):
            if db_write("""UPDATE users SET verified= %s WHERE email = %s""",
                (True, user_email),):
                return Response(status=200)
            else:
                jsonify({"error": "verification_error"}), 401
        else:
            return jsonify({"error": "verification_error"}), 401
    else:
        return jsonify({"error": "verified"}), 401

@authentication.route("/resend_verification", methods=["POST"])
def resend_verification():
    print(request.json)
    user_email = request.json["email"]
    first_name = request.json["first_name"]
    new_verification_code = randint(10000, 99999)
    verified = check_if_verified(user_email)
    if not verified:
        if db_write("""UPDATE users SET verification_code= %s WHERE email = %s""",
            (new_verification_code, user_email),):

            send_verification_email(user_email, first_name, new_verification_code)
            return Response(status=200)
        else:
            return jsonify({"error": "failed"}), 401

        
    else:
        return jsonify({"error": "verified"}), 401

