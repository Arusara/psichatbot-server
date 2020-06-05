from utils import db_read, db_write
import datetime


##DATA PACKAGES
def activate_data_package(name, user_id):
    package_id = get_data_package(name)["id"]
    activated_date = datetime.datetime.now()
    if not check_data_package_already_activated(user_id):
        if db_write(
                """INSERT INTO user_data_package (package_id, user_id, package_name, activated_date) 
                VALUES (%s, %s, %s, %s)""", (package_id, user_id, name, activated_date)):
            remaining_data = get_data_package(name)["data"]
            return name + " package has been successfully activated. You now have " + str(
                remaining_data) + "MB remaining"
        else:
            return "Data package activation failed. Please try again."

    else:
        return "You have already activated a package. Please opt to change your package instead."


def change_data_package(name, user_id):
    package_id = get_data_package(name)["id"]
    activated_date = datetime.datetime.now()
    if check_data_package_already_activated(user_id):
        if db_write(
                """UPDATE user_data_package 
                SET package_id=%s, package_name=%s, data_used=%s, activated_date=%s 
                WHERE user_id=%s""",
                (package_id, name, 0, activated_date, user_id)):
            remaining_data = get_data_package(name)["data"]
            return " Your data package has been successfully changed to " + name + ". You now have " + str(
                remaining_data) + "MB reamining"
        else:
            return "Failed to change data package. Please try again"
    else:
        return "You have no currently activated data package. Please opt to activate a new package instead."


def deactivate_data_package(user_id):
    if check_data_package_already_activated(user_id):
        if db_write("""DELETE FROM user_data_package WHERE user_id = %s""", (user_id,)):
            return "Your data package has been successfully deactivated"
        else:
            return "Data package deactivation failed. Please try again"
    else:
        return "You have no currently activated data packages"


##VOICE PACKAGES
def activate_voice_package(name, user_id):
    package_id = get_voice_package(name)["id"]
    activated_date = datetime.datetime.now()
    if not check_voice_package_already_activated(user_id):
        if db_write(
                """INSERT INTO user_voice_package (package_id, user_id, package_name, activated_date) VALUES (%s, %s, %s, %s)""",
                (package_id, user_id, name, activated_date)):
            remaining_minutes = get_voice_package(name)["minutes"]
            return name + " package has been successfully activated. You now have " + str(
                remaining_minutes) + " minutes reamining"
        else:
            return "Voice package activation failed. Please try again."

    else:
        return "You have already activated a voice package. Please opt to change your package instead."


def change_voice_package(name, user_id):
    package_id = get_voice_package(name)["id"]
    activated_date = datetime.datetime.now()
    if check_voice_package_already_activated(user_id):
        if db_write(
                """UPDATE user_voice_package SET package_id=%s, package_name=%s, minutes_used=%s, activated_date=%s WHERE user_id=%s""",
                (package_id, name, 0, activated_date, user_id)):
            remaining_minutes = get_voice_package(name)["minutes"]
            return " Your voice package has been successfully changed to " + name + ". You now have " + str(
                remaining_minutes) + " minutes reamining"
        else:
            return "Failed to change voice package. Please try again"
    else:
        return "You have no currently activated voice package. Please opt to activate a new package instead."


def deactivate_voice_package(user_id):
    if check_voice_package_already_activated(user_id):
        if db_write("""DELETE FROM user_voice_package WHERE user_id = %s""", (user_id,)):
            return "Your voice package has been successfully deactivated"
        else:
            return "Voice package deactivation failed. Please try again"
    else:
        return "You have no currently activated voice packages"


##Data Packages
def check_data_package_name(name):
    package_name = db_read("""SELECT name FROM data_packages WHERE name = %s""", (name,))

    if package_name:
        if package_name[0]["name"] == name:
            return True
        else:
            return False
    else:
        return False


def get_data_packages():
    packages = db_read("""SELECT * FROM data_packages """)
    return packages


def get_data_package(package_name):
    package = db_read("""SELECT * FROM data_packages WHERE name= %s""", (package_name,))
    return package[0]


def check_data_package_already_activated(user_id):
    users = db_read("""SELECT user_id FROM user_data_package WHERE user_id = %s""", (user_id,))
    if users:
        return True
    else:
        return False


##Voice Packages
def check_voice_package_name(name):
    package_name = db_read("""SELECT name FROM voice_packages WHERE name = %s""", (name,))

    if package_name:
        if package_name[0]["name"] == name:
            return True
        else:
            return False
    else:
        return False


def get_voice_packages():
    packages = db_read("""SELECT * FROM voice_packages """)
    return packages


def get_voice_package(package_name):
    package = db_read("""SELECT * FROM voice_packages WHERE name= %s""", (package_name,))
    return package[0]


def check_voice_package_already_activated(user_id):
    users = db_read("""SELECT user_id FROM user_voice_package WHERE user_id = %s""", (user_id,))
    if users:
        return True
    else:
        return False


##USAGE DATA

def get_data_usage_data(user_id):
    usage_data = db_read(
        """SELECT package_name, data_used, activated_date, data, valid_period FROM user_data_package, data_packages WHERE user_id = %s AND user_data_package.package_id = data_packages.id""",
        (user_id,))

    if usage_data:
        current_date = datetime.datetime.now()
        activated_date = usage_data[0]["activated_date"]
        valid_period = usage_data[0]["valid_period"]
        remaining_days = str(int(valid_period - ((current_date - activated_date).days)) - 1) + " days " + str(
            24 - (current_date - activated_date).seconds // 3600) + " hours " + str(
            60 - ((current_date - activated_date).seconds // 60) % 60) + " minutes"
        usage = "Active data package: " + usage_data[0]["package_name"] + "\n" + \
                "Remaining data: " + str((usage_data[0]["data"] - usage_data[0]["data_used"])) + "MB\n" + \
                "Remaining days: " + remaining_days
        return usage
    else:
        if check_data_package_already_activated(user_id):
            return "Usage data retrival failed. Please contact system administrator"
        else:
            return "You have no currently activated data packages"


def get_voice_usage_data(user_id):
    usage_data = db_read(
        """SELECT package_name, minutes_used, activated_date, minutes, valid_period FROM user_voice_package, voice_packages WHERE user_id = %s AND user_voice_package.package_id = voice_packages.id""",
        (user_id,))

    if usage_data:
        current_date = datetime.datetime.now()
        activated_date = usage_data[0]["activated_date"]
        valid_period = usage_data[0]["valid_period"]
        remaining_days = str(int(valid_period - ((current_date - activated_date).days)) - 1) + " days " + str(
            24 - (current_date - activated_date).seconds // 3600) + " hours " + str(
            60 - ((current_date - activated_date).seconds // 60) % 60) + " minutes"
        usage = "Active voice package: " + usage_data[0]["package_name"] + "\n" + \
                "Remaining talktime: " + str(
            int((usage_data[0]["minutes"] - usage_data[0]["minutes_used"]))) + " minutes\n" + \
                "Remaining days: " + remaining_days
        return usage
    else:
        if check_voice_package_already_activated(user_id):
            return "Usage data retrival failed. Please contact system administrator"
        else:
            return "You have no currently activated voice packages"
