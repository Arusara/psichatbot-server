from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

# Language processing
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import extract_info

# Machine Learning
import numpy
import tflearn
import random
import json
import pickle


# from tensorflow.python.util import deprecation
# deprecation._PRINT_DEPRECATION_WARNINGS = False

import tensorflow


#chatbot functions
from chatbot_functions import new_data_package, \
    new_data_package_name,\
    new_voice_package, new_voice_package_name,\
    deactivate_data_confirmation, deactivate_voice_confirmation, deactivate_package,\
    no_signal, no_signal_location, low_signal, low_signal_location,\
    data_usage_data, voice_usage_data, usage_data,\
    chatbot_functions_detail,\
    get_data_package_info, get_voice_package_info, get_package_details,\
    change_data_package_function, change_voice_package_function,\
    change_data_package_name, change_voice_package_name


tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)


with open("intents.json") as file:
    data = json.load(file)

try:
    x=t
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
            if intent["tag"] not in labels:
                labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        
        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)


"""Change here to train Model after editing intents"""
try:  # Loads the current model (if it exists)
    #If the intents.json file has been changed, then comment out model.load("model.tflearn"), and bring back the 'raise Exception'
    model.load("model.tflearn")
    #raise Exception
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return numpy.array(bag)

def classify(message):
    results = model.predict([bag_of_words(message, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[results_index] > 0.7:
        for tg in data["intents"]:
            if tg["tag"] == tag:
                return tg
    else:
        return False

def prep_for_extract(message):  # Prepares the message for information extraction returning an nltk Tree
    sent = message
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    
    tree = nltk.ne_chunk(sent)
    return tree

# context = {}  # Holds the context for each user as a dictionary with key-value pairs as "userId": "context"

def response(inp, userId, context_user):  # Returns the bot's response for "inp"
    context={}
    context[userId] = context_user
    if userId in context.keys():
        if context[userId] == "new package name":
            tree = prep_for_extract(inp)
            package = extract_info.package(tree)
            if package != None:
                print(package + " new package name")
                context[userId] = ""
                while context[userId]!= "":
                    pass
                return "Okay, I'll activate " + package + " for you. Context:" + context[userId], context[userId]
            else:
                return "I'm sorry but that's not a valid package name. Please try again. Context:" + context[userId] , context[userId]
        elif context[userId] == "change package name":
            tree = prep_for_extract(inp)
            package = extract_info.package(tree)
            if package != None:
                print(package + " change package name")
                context[userId] = ""
                while context[userId]!= "":
                    pass
                return "Okay, I'll change your package to " + package +"Context:" + context[userId], context[userId]
            else:
                return "I'm sorry but that's not a valid package name. Please try again. Context:" + context[userId], context[userId]
        elif context[userId] == "deactivate package":
            return deactivate_package(inp, userId, context[userId])
        elif context[userId] == "continue":
            context[userId] = ""
            if "no" in inp.lower():
                return "Goodbye", context[userId]
        elif context[userId] == "new data package name":
            if inp.lower() != "cancel":
                tree = prep_for_extract(inp)
                return new_data_package_name(tree, context[userId], userId)
            else:
                context[userId] = ""
                return "Action cancelled", context[userId]
        elif context[userId] == "new voice package name":
            if inp.lower() != "cancel":
                tree = prep_for_extract(inp)
                return new_voice_package_name(tree, context[userId], userId)
            else:
                context[userId] = ""
                return "Action cancelled", context[userId]
        elif context[userId] == "deactivate data package":
            return deactivate_data_confirmation(inp, userId, context[userId])
        elif context[userId] == "deactivate voice package":
            return deactivate_voice_confirmation(inp, userId, context[userId])
        elif context[userId] == "no signal location":
            tree = prep_for_extract(inp)
            return no_signal_location(tree,userId, context[userId])
        elif context[userId] == "low signal location":
            tree = prep_for_extract(inp)
            return low_signal_location(tree,userId, context[userId])
        elif context[userId] == "change data package name":
            tree = prep_for_extract(inp)
            return change_data_package_name(tree, context[userId], userId)
        elif context[userId] == "change voice package name":
            tree = prep_for_extract(inp)
            return change_voice_package_name(tree, context[userId], userId)





    i = classify(inp)
    if i:  # Checks whether the classification worked (If it didn't work, "i" would be "False")
        
        
        if (not 'context_filter' in i) or (userId in context and 'context_filter' in i and i['context_filter'] == context[userId]):  # Checking for context

            if 'context_set' in i:  # Checks whether the classification requires context to be set
                print('context:', i['context_set'])
                context[userId] = i['context_set']

            # Information extraction
            tree = prep_for_extract(inp)
            if i['tag']=="greeting":
                return "Hi there, how can I help you?\n\n" + chatbot_functions_detail(), context[userId]
            elif i['tag']=="no signal":
                return no_signal(tree, userId, context[userId])
            elif i['tag']=="low signal":
                return low_signal(tree, userId, context[userId])
            elif i['tag']=="change package":
                package = extract_info.package(tree)
                if package:
                    return "Okay, I'll change your package to " + package, context[userId]
                else:
                    context[userId] = "change package name"
                    while context[userId]!= "change package name":
                        pass
                    return "Which package do you want to change to? Context:" + context[userId], context[userId]
            elif i['tag']=="new package":
                package = extract_info.package(tree)
                if package:
                    return "Okay, I'll activate " + package + " for you", context[userId]
                else:
                    context[userId] = "new package name"
                    while context[userId]!= "new package name":
                        pass
                    return "Which package do you want to activate? Context:" + context[userId], context[userId]
            elif i['tag']=="new data package":
                return new_data_package(tree,context[userId], userId)
            elif i['tag']=="new voice package":
                return new_voice_package(tree,context[userId], userId)
            elif i['tag']=="data usage data":
                return data_usage_data(userId), context[userId]
            elif i['tag']=="voice usage data":
                return voice_usage_data(userId), context[userId]
            elif i['tag']=="usage data":
                return usage_data(userId), context[userId]
            elif i['tag']=="chatbot functions":
                return chatbot_functions_detail(), context[userId]
            elif i['tag']=="request data package info":
                return get_data_package_info(), context[userId]
            elif i['tag']=="request voice package info":
                return get_voice_package_info(), context[userId]
            elif i['tag']=="request package info":
                return get_package_details(tree, context[userId])
            elif i['tag']=="change data package":
                return change_data_package_function(tree, context[userId], userId)
            elif i['tag']=="change voice package":
                return change_voice_package_function(tree, context[userId], userId)




            responses = i["responses"]
            return random.choice(responses),  context[userId]
        else:  # The context didn't match
            return "I'm sorry, I didn't get that. Please try again. Context:" + context[userId], context[userId]
    else:  # The classification didn't work
        return "I'm sorry, I didn't get that. Please try again. Context:" + context[userId], context[userId]


