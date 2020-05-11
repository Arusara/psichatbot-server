from utils import db_read, db_write
import datetime

# def deactivate_package():

def activate_package(name, user_id):
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


# def activate_voice_package():

# def deactivate_voice_package():

# def activate_data_package():

# def deactivate_data_package():

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
