from utils import db_read, db_write
import datetime

def report_no_signal(user_id, location):
    report = "User has reported loss of signal. \nUser ID: "+ str(user_id) +"\nLocation: "+ location
    current_date  = datetime.datetime.now()
    if db_write("""INSERT INTO user_complaint_no_signal (user_id, location, report, date) VALUES (%s,%s,%s,%s)""", (user_id, location, report,current_date)):
        return True
    else:
        return False

def report_low_signal(user_id, location):
    report = "User has reported weak signal. \nUser ID: "+ str(user_id) +"\nLocation: "+ location
    current_date  = datetime.datetime.now()
    if db_write("""INSERT INTO user_complaint_low_signal (user_id, location, report, date) VALUES (%s,%s,%s,%s)""", (user_id, location, report,current_date)):
        return True
    else:
        return False