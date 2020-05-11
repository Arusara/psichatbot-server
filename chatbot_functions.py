from extract_info import ne_low_signal_location, ne_change_package, ne_package, ne_name, ne_data_package, ne_voice_package

from package_management import check_data_package_name, get_data_packages, get_data_package, activate_package

# def no_signal(tree):
#     location = low_signal_location(tree)
#     if location:
#         #context[userId] = "no signal description"
#         return "We will look into the loss of signal in " + location + ". Thank you for staying with our network."
#     else:
#         context[userId] = "no signal location"
#         while context[userId]!= "no signal location":
#             pass
#         return "Where did you face difficulties connecting to our network?"

# def low_signal(tree):
#     location = low_signal_location(tree)
#     if location:
#         #context[userId] = "no signal description"
#         return "We will look into the loss of signal in " + location + ". Thank you for staying with our network."
#     else:
#         context[userId] = "no signal location"
#         while context[userId]!= "no signal location":
#             pass
#         return "Where did you face difficulties connecting to our network?"

# # """Change packages"""
# def change_data_package(tree):
#     package = extract_info.package(tree)
#     if package:
#         return "Okay, I'll change your data package to " + package
#     else:
#         context[userId] = "change data package name"
#         # while context[userId]!= "change data package name":
#         #     pass
#         return "Which package do you want to change to? Context:" + context[userId]

# def change_data_package_name(tree):
#     package = extract_info.package(tree)
#     if package != None:
#         print(package + " change data package name")
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay, I'll change your data package to " + package +"Context:" + context[userId]
#     else:
#         return "I'm sorry but that's not a valid package name. Please try again. Context:" + context[userId]

# def change_voice_package(tree):
#     package = extract_info.package(tree)
#     if package:
#         return "Okay, I'll change your voice package to " + package
#     else:
#         context[userId] = "change voice package name"
#         # while context[userId]!= "change package name":
#         #     pass
#         return "Which package do you want to change to? Context:" + context[userId]

# def change_voice_package_name(tree):
#     package = extract_info.package(tree)
#     if package != None:
#         print(package + " change voice package name")
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay, I'll change your data package to " + package +"Context:" + context[userId]
#     else:
#         return "I'm sorry but that's not a valid package name. Please try again. Context:" + context[userId]

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


# """Activate new packages"""
def new_data_package(tree, user_context, user_id):
    package_name = ne_data_package(tree)
    data_packages_list = get_data_packages()
    data_packages_string=""
    for i in data_packages_list: 
        data_packages_string+= i["name"] + ",\n "
    if package_name:
        if check_data_package_name(package_name):
            return activate_package(package_name, user_id), user_context 
        else:
            user_context = "new data package name"
            return "I'm sorry but that's not a valid data package. These are the available data packages \n" + data_packages_string, user_context
    else:
        user_context = "new data package name"
        return "Which data package do you want to activate? \n" + data_packages_string, user_context

# def new_data_package_name(tree):
#     package = extract_info.package(tree)
#     if package != None:
#         print(package + " new data package name")
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay, I'll activate " + package + " for you. Context:" + context[userId]
#     else:
#         return "I'm sorry but that's not a valid data package name. Please try again. Context:" + context[userId]

# def new_voice_package(tree):
#     package = extract_info.package(tree)
#     if package:
#         return "Okay, I'll activate " + package + " for you"
#     else:
#         context[userId] = "new voice package name"
#         while context[userId]!= "new voice package name":
#             pass
#         return "Which voice package do you want to activate?"

# def new_voice_package_name(tree):
#     package = extract_info.package(tree)
#     if package != None:
#         print(package + " new voice package name")
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay, I'll activate " + package + " for you. Context:" + context[userId]
#     else:
#         return "I'm sorry but that's not a valid voice package name. Please try again. Context:" + context[userId]

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

# # """Deactivate packages"""
# def deactivate_data_package():
#     #deactivate data

# def deactivate_voice_package():
#     #deactivate voice

# def deactivate_data_confirmation(inp):
#     if "yes" in inp.lower():
#         deactivate_data_package()
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay. I will deactivate your data package"
#     else:
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay. Is there anything else I can help you with?"

# def deactivate_voice_confirmation(inp):
#     if "yes" in inp.lower():
#         deactivate_voice_package()
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay. I will deactivate your voice package"
#     else:
#         context[userId] = ""
#         while context[userId]!= "":
#             pass
#         return "Okay. Is there anything else I can help you with?"

# def deactivate_package_confirmation(inp):


# def deactivate_package(tree, inp):
#     if context[userId] = "deactivate package":
#         context[userId] = "deactivate package name"
#         while context[userId]!= "deactivate package name":
#             pass
#         return "Which package do you want to deactivate? Voice or Data? Context:" + context[userId]

#     else if context[userId] = "deactivate package name":
#         if inp = "Data":
#             deactivate_data_package()
#             context[userId] = ""
#         else if inp = "Voice":
#             deactivate_voice_package()
#             context[userId] = ""
#         else:
#             return "I'm sorry I didn't understand that. Could you please let me know which package Voice or Data you'd like to deactivate"
