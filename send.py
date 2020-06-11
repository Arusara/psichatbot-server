from flask import Flask, render_template
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)
mail = Mail(app)

def send_verification_email(email, first_name, verification_code):
    msg = Message(subject="Email Verification - PSIS",
                    sender= app.config["MAIL_USERNAME"],
                    recipients=[email])
    msg.html = render_template("template.html", first_name= first_name, verification_code = verification_code)
    mail.send(msg)

with app.app_context(): 
    send_verification_email("lordpakeersl@gmail.com", "Minul", 98764)
