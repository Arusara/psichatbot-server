from extract_info import ne_low_signal_location, ne_change_package, ne_package, ne_name, ne_data_package, ne_voice_package

from package_management import check_data_package_name, get_data_packages,\
    get_data_package, activate_data_package, check_voice_package_name, get_voice_packages, get_voice_package, activate_voice_package,\
    deactivate_data_package, deactivate_voice_package,\
    get_data_usage_data, get_voice_usage_data,\
    change_data_package, change_voice_package

from complaint_handler import report_no_signal, report_low_signal

#NO SIGNAL COMPLAINT
def no_signal(tree, user_id, user_context):
    location = ne_low_signal_location(tree)
    if location:
        user_context = ""
        if report_no_signal(user_id, location):
            return "We will look into the loss of signal in " + location + ". Thank you for staying with our network.", user_context
        else:
            return "Error reporting loss of signal.", user_context
    else:
        user_context = "no signal location"

        return "Where did you face difficulties connecting to our network?", user_context

def no_signal_location(tree, user_id, user_context):
    location = ne_low_signal_location(tree)
    if location:
        user_context = ""
        if report_no_signal(user_id, location):
            return "We will look into the loss of signal in " + location + ". Thank you for staying with our network.", user_context
        else:
            return "Error reporting loss of signal.", user_context
    else:
        return "Please restate where you faced difficulties connecting to our network", user_context

#LOW SIGNAL COMPLAINT
def low_signal(tree, user_id, user_context):
    location = ne_low_signal_location(tree)
    if location:
        user_context = ""
        if report_low_signal(user_id, location):
            return "We will look into the weak signal in " + location + ". Thank you for staying with our network.", user_context
        else:
            return "Error reporting weak signal.", user_context
    else:
        user_context = "low signal location"

        return "Where did you face difficulties connecting to our network?", user_context

def low_signal_location(tree, user_id, user_context):
    location = ne_low_signal_location(tree)
    if location:
        user_context = ""
        if report_low_signal(user_id, location):
            return "We will look into the weak signal in " + location + ". Thank you for staying with our network.", user_context
        else:
            return "Error reporting weak signal.", user_context
    else:
        return "Please restate where you faced difficulties connecting to our network", user_context


# """Change packages"""
def change_data_package_function(tree, user_context, user_id):
    package_name = ne_data_package(tree)
    data_packages_list = get_data_packages()
    data_packages_string=""
    for i in data_packages_list: 
        data_packages_string+= i["name"] +"-("+ str(i["data"])+ "MB, "+ str(i["valid_period"]).split(".")[0]+ "days)\n"
    if package_name:
        if check_data_package_name(package_name):
            return change_data_package(package_name, user_id), user_context 
        else:
            user_context = "change data package name"
            return "I'm sorry but that's not a valid data package. These are the available data packages \n" + data_packages_string, user_context
    else:
        user_context = "change data package name"
        return "Which data package do you want to change to? \n" + data_packages_string, user_context

def change_data_package_name(tree, user_context, user_id):
    package_name = ne_data_package(tree)
    data_packages_list = get_data_packages()
    data_packages_string=""
    for i in data_packages_list: 
        data_packages_string+= i["name"] +"-("+ str(i["data"])+ "MB, "+ str(i["valid_period"]).split(".")[0]+ "days)\n"
    if package_name:
        if check_data_package_name(package_name):
            user_context = ""
            return change_data_package(package_name, user_id), user_context 
        else:
            return "I'm sorry but that's not a valid data package. These are the available data packages \n" + data_packages_string, user_context
    else:
        return "I'm sorry but that's not a valid data package name. Please try again. These are the available data packages \n" + data_packages_string, user_context

def change_voice_package_function(tree, user_context, user_id):
    package_name = ne_voice_package(tree)
    voice_packages_list = get_voice_packages()
    voice_packages_string=""
    for i in voice_packages_list: 
        voice_packages_string+= i["name"] +"-("+ str(i["minutes"]) + "minutes, "+str(i["valid_period"]).split(".")[0] +"days)\n"
    if package_name:
        if check_voice_package_name(package_name):
            return change_voice_package(package_name, user_id), user_context 
        else:
            user_context = "change voice package name"
            return "I'm sorry but that's not a valid voice package. These are the available voice packages \n" + voice_packages_string, user_context
    else:
        user_context = "change voice package name"
        return "Which voice package do you want to change to? \n" + voice_packages_string, user_context

def change_voice_package_name(tree, user_context, user_id):
    package_name = ne_voice_package(tree)
    voice_packages_list = get_voice_packages()
    voice_packages_string=""
    for i in voice_packages_list: 
        voice_packages_string+= i["name"] +"-("+ str(i["minutes"]) + "minutes, "+str(i["valid_period"]).split(".")[0] +"days)\n"
    if package_name:
        if check_voice_package_name(package_name):
            user_context = ""
            return change_voice_package(package_name, user_id), user_context 
        else:
            return "I'm sorry but that's not a valid voice package. These are the available voice packages \n" + voice_packages_string, user_context
    else:
        return "I'm sorry but that's not a valid voice package name. Please try again.", user_context

# def change_package_name(tree):
#     package = extract_info.package(tree)
#     if package != None:
#         print(package + " change package name")
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay, I'll change your package to " + package +"Context:" + context[userId]
#     else:
#         return "I'm sorry but that's not a valid package name. Please try again. Context:" + context[userId]


#ACTIVATE NEW PACKAGES
def new_data_package(tree, user_context, user_id):
    package_name = ne_data_package(tree)
    data_packages_list = get_data_packages()
    data_packages_string=""
    for i in data_packages_list: 
        data_packages_string+= i["name"] +"-("+ str(i["data"])+ "MB, "+ str(i["valid_period"]).split(".")[0]+ "days)\n"
    if package_name:
        if check_data_package_name(package_name):
            return activate_data_package(package_name, user_id), user_context 
        else:
            user_context = "new data package name"
            return "I'm sorry but that's not a valid data package. These are the available data packages \n" + data_packages_string, user_context
    else:
        user_context = "new data package name"
        return "Which data package do you want to activate? \n" + data_packages_string, user_context

def new_data_package_name(tree,user_context, user_id):
    package_name = ne_data_package(tree)
    data_packages_list = get_data_packages()
    data_packages_string=""
    for i in data_packages_list: 
        data_packages_string+= i["name"] +"-("+ str(i["data"])+ "MB, "+ str(i["valid_period"]).split(".")[0]+ "days)\n"
    if package_name:
        if check_data_package_name(package_name):
            user_context = ""
            return activate_data_package(package_name, user_id), user_context 
        else:
            return "I'm sorry but that's not a valid data package. These are the available data packages \n" + data_packages_string, user_context
    else:
        return "I'm sorry but that's not a valid data package name. Please try again. Context:" + user_context, user_context

def new_voice_package(tree, user_context, user_id):
    package_name = ne_voice_package(tree)
    voice_packages_list = get_voice_packages()
    voice_packages_string=""
    for i in voice_packages_list: 
        voice_packages_string+= i["name"] +"-("+ str(i["minutes"]) + "minutes, "+str(i["valid_period"]).split(".")[0] +"days)\n"
    if package_name:
        if check_voice_package_name(package_name):
            return activate_voice_package(package_name, user_id), user_context 
        else:
            user_context = "new voice package name"
            return "I'm sorry but that's not a valid voice package. These are the available voice packages \n" + voice_packages_string, user_context
    else:
        user_context = "new voice package name"
        return "Which voice package do you want to activate? \n" + voice_packages_string, user_context

def new_voice_package_name(tree,user_context, user_id):
    package_name = ne_voice_package(tree)
    voice_packages_list = get_voice_packages()
    voice_packages_string=""
    for i in voice_packages_list: 
        voice_packages_string+= i["name"] +"-("+ str(i["minutes"]) + "minutes, "+str(i["valid_period"]).split(".")[0] +"days)\n"
    if package_name:
        if check_voice_package_name(package_name):
            user_context = ""
            return activate_voice_package(package_name, user_id), user_context 
        else:
            return "I'm sorry but that's not a valid voice package. These are the available voice packages \n" + voice_packages_string, user_context
    else:
        return "I'm sorry but that's not a valid voice package name. Please try again. Context:" + user_context, user_context

# def new_package(tree):
#     package = extract_info.package(tree)
#     if package:
#         return "Okay, I'll activate " + package + " for you"
#     else:
#         context[userId] = "new package name"
#         while context[userId]!= "new package name":
#             pass
#         return "Which package do you want to activate?"

# def new_package_name(tree):
#     package = extract_info.package(tree)
#     if package != None:
#         print(package + " new package name")
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay, I'll activate " + package + " for you. Context:" + context[userId]
#     else:
#         return "I'm sorry but that's not a valid package name. Please try again. Context:" + context[userId]

#DEACTIVATE PACKAGES
def deactivate_data_confirmation(inp, user_id, user_context):
    if "yes" in inp.lower():
        user_context = ""
        return deactivate_data_package(user_id), user_context
    elif "no" in inp.lower():
        user_context = "continue"
        return "Okay. Is there anything else I can help you with?", user_context
    else:
        return "I'm sorry I didn't get that. Please answer with yes or no.", user_context

def deactivate_voice_confirmation(inp, user_id, user_context):
    if "yes" in inp.lower():
        user_context = ""
        return deactivate_voice_package(user_id), user_context
    elif "no" in inp.lower():
        user_context = "continue"
        return "Okay. Is there anything else I can help you with?", user_context
    else:
        return "I'm sorry I didn't get that. Please answer with yes or no.", user_context

def deactivate_package(inp, user_id, user_context):
    if "data" in inp.lower():
        user_context = "deactivate data package"
        return "Are you sure you want to deactivate your data package?", user_context
    elif "voice" in inp.lower():
        user_context = "deactivate voice package"
        return "Are you sure you want to deactivate your voice package?", user_context
    else:
        return "I'm sorry I didn't understand that. Could you let me know which package Voice or Data you'd like to deactivate?", user_context



#USAGE DATA

def data_usage_data(user_id):
    return get_data_usage_data(user_id)

def voice_usage_data(user_id):
    return get_voice_usage_data(user_id)

def usage_data(user_id):
    data_usage = get_data_usage_data(user_id)
    voice_usage = get_voice_usage_data(user_id)
    usage = "Data package usage\n" +\
            "----------------------------------\n" +\
            data_usage +\
            "\n\nVoice package usage\n"+\
                "-----------------------------------\n"+\
            voice_usage
    return usage


##PACKAGE INFORMATION

def get_data_package_info():
    data_packages_list = get_data_packages()
    data_packages_string=""
    for i in data_packages_list: 
        data_packages_string+= i["name"] +"-("+ str(i["data"])+ "MB, "+ str(i["valid_period"]).split(".")[0]+ "days, Rs. "+str(i["price"])+ " )\n"

    return "Here are the available data packages. \n\n"+data_packages_string    


def get_voice_package_info():
    voice_packages_list = get_voice_packages()
    voice_packages_string=""
    for i in voice_packages_list: 
        voice_packages_string+= i["name"] +"-("+ str(i["minutes"]).split(".")[0] + "minutes, "+str(i["valid_period"]).split(".")[0] +"days, Rs. "+str(i["price"]) +" )\n"
    return "Here are the available voice packages. \n\n"+ voice_packages_string

def get_package_details(tree, user_context):
    package_name = ne_voice_package(tree)
    if package_name:
        if check_data_package_name(package_name):
            i = get_data_package(package_name)
            package_details = i["name"] +"\nAvailable data:"+ str(i["data"])+ "MB\nValid period:"+ str(i["valid_period"]).split(".")[0]+ "days \nPrice: Rs. "+str(i["price"])
            return "Here are the details of the data package\n\n" + package_details, user_context
        elif check_voice_package_name(package_name):
            i = get_voice_package(package_name)
            package_details = i["name"] +"\nAvailable talktime:"+ str(i["minutes"]).split(".")[0] + "minutes\nValid period: "+str(i["valid_period"]).split(".")[0] +"days\nPrice: Rs. "+str(i["price"])
            return "Here are the details of the voice package\n\n" + package_details, user_context
        else:
            return "That is not a valid package name", user_context
    else:
        return "Here are all the available package\n\n"+ get_data_package_info()+"\n\n"+get_voice_package_info(), user_context 

##CHATBOT FUNCTIONS
def chatbot_functions_detail():
    functions = "Here are some of the things I can do.\n"+\
                "1. Activate, Change or Deactivate data or voice packages\n"+\
                "   Eg: I want to activate <package name> data package. I want to change my voice package. I want to deactivate my data package.\n\n" +\
                "2. Complain about the loss of signal or low signal\n"+\
                "   Eg: There is no signal. I am not getting any signal. Internet is slow. The signal is weak\n\n"+\
                "3. View usage data\n"+\
                "   Eg: View data usage. How many minutes do I have left? Show me my voice package usage\n\n"+\
                "4. View package information\n"+\
                "   Eg: Show me the details of data packages. Show me the details of <package name> package. Show me the details of packages\n"
                
    return functions