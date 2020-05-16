from utils import db_read, db_write
import datetime

# def deactivate_package():

def activate_data_package(name, user_id):
    package_id = get_data_package(name)["id"]
    activated_date = datetime.datetime.utcnow()
    if check_data_package_already_activated(user_id):
        if db_write("""INSERT INTO user_data_package (package_id, user_id, package_name, activated_date) VALUES (%s, %s, %s, %s)""",(package_id, user_id, name, activated_date)):
            remaining_data = get_data_package(name)["data"]
            return name+ " package has been successfully activated. You now have " +str(remaining_data)+ "MB reamining"
        else:
            return "Data package activation failed. Please try again."
    
    else:
        return "You have already activated a package. Please opt to change your package instead."


def activate_voice_package(name, user_id):
    package_id = get_voice_package(name)["id"]
    activated_date = datetime.datetime.utcnow()
    if check_voice_package_already_activated(user_id):
        if db_write("""INSERT INTO user_voice_package (package_id, user_id, package_name, activated_date) VALUES (%s, %s, %s, %s)""",(package_id, user_id, name, activated_date)):
            remaining_minutes = get_voice_package(name)["minutes"]
            return name+ " package has been successfully activated. You now have " +str(remaining_minutes)+ " minutes reamining"
        else:
            return "Voice package activation failed. Please try again."
    
    else:
        return "You have already activated a voice package. Please opt to change your package instead."

# def deactivate_voice_package():

# def activate_data_package():

# def deactivate_data_package():


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
        return False
    else:
        return True


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
        return False
    else:
        return True