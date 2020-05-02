from extract_info import low_signal_location, change_package, package, name

def no_signal(tree):
    location = low_signal_location(tree)
    if location:
        #context[userId] = "no signal description"
        return "We will look into the loss of signal in " + location + ". Thank you for staying with our network."
    else:
        context[userId] = "no signal location"
        while context[userId]!= "no signal location":
            pass
        return "Where did you face difficulties connecting to our network?"

def low_signal(tree):
    location = low_signal_location(tree)
    if location:
        #context[userId] = "no signal description"
        return "We will look into the loss of signal in " + location + ". Thank you for staying with our network."
    else:
        context[userId] = "no signal location"
        while context[userId]!= "no signal location":
            pass
        return "Where did you face difficulties connecting to our network?"
"""Change packages"""
def change_data_package(tree):
    package = extract_info.package(tree)
    if package:
        return "Okay, I'll change your data package to " + package
    else:
        context[userId] = "change data package name"
        # while context[userId]!= "change data package name":
        #     pass
        return "Which package do you want to change to? Context:" + context[userId]

def change_voice_package(tree):
    package = extract_info.package(tree)
    if package:
        return "Okay, I'll change your voice package to " + package
    else:
        context[userId] = "change voice package name"
        # while context[userId]!= "change package name":
        #     pass
        return "Which package do you want to change to? Context:" + context[userId]


"""Activate new packages"""
def new_data_package(tree):
    package = extract_info.package(tree)
    if package:
        return "Okay, I'll activate " + package + " for you"
    else:
        context[userId] = "new data package name"
        while context[userId]!= "new data package name":
            pass
        return "Which data package do you want to activate? "

def new_voice_package(tree):
    package = extract_info.package(tree)
    if package:
        return "Okay, I'll activate " + package + " for you"
    else:
        context[userId] = "new voice package name"
        while context[userId]!= "new voice package name":
            pass
        return "Which voice package do you want to activate?"

"""Deactivate packages"""
def deactivate_data_package():
    #deactivate data

def deactivate_voice_package():
    #deactivate voice

