# Language processing
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import extract_info

# Machine Learning
import numpy
import tflearn
import tensorflow
import random
import json
import pickle

# Flask
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
import datetime

app = Flask(__name__)

#GET /
@app.route('/', methods=["GET"])
@cross_origin()
def testGet():
    return jsonify({"userId": 1,"isBot": True}), 200

# POST /telecomchatbot
@app.route('/', methods=["POST"])
@cross_origin()
def chatbotReply():
    global context
    message = request.get_json()
    messageText = message['message']
    userId = message['userId']
    if not userId in context.keys():
        context[userId]=""
    while userId not in context.keys():
        pass
    reply = response(messageText, userId)
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    ident = json.dumps(datetime.datetime.now(), default=date_handler).strip('"')
    return jsonify({"userId": 1, "id": ident, "message": reply, "isBot": True}), 200


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

context = {}  # Holds the context for each user as a dictionary with key-value pairs as "userId": "context"

def response(inp, userId):  # Returns the bot's response for "inp"
    global context

    if userId in context.keys():
        if context[userId] == "new package name":
            tree = prep_for_extract(inp)
            package = extract_info.package(tree)
            if package != None:
                print(package + " new package name")
                context[userId] = ""
                while context[userId]!= "":
                    pass
                return "Okay, I'll activate " + package + " for you. Context:" + context[userId]
            else:
                return "I'm sorry but that's not a valid package name. Please try again. Context:" + context[userId]
        elif context[userId] == "change package name":
            tree = prep_for_extract(inp)
            package = extract_info.package(tree)
            if package != None:
                print(package + " change package name")
                context[userId] = ""
                while context[userId]!= "":
                    pass
                return "Okay, I'll change your package to " + package +"Context:" + context[userId]
            else:
                return "I'm sorry but that's not a valid package name. Please try again. Context:" + context[userId]
        elif context[userId] == "deactivate package":
            if "yes" in inp.lower():
                context[userId] = ""
                while context[userId]!= "":
                    pass
                return "Okay. I will deactivate the package"
            else:
                context[userId] = ""
                while context[userId]!= "":
                    pass
                return "Okay. Is there anything else I can help you with?"
        elif context[userId] == "no signal location":
            tree = prep_for_extract(inp)
            location = extract_info.low_signal_location(tree)
            if location:
                context[userId] = ""
                while context[userId]!= "":
                    pass
                return "We will look into the loss of signal in " + location + ". Thank you for staying with our network."
            else:
                return "I'm sorry, I didn't get that. Please try again."
        elif context[userId] == "continue":
            context[userId] = ""
            while context[userId]!= "":
                pass
            if "no" in inp.lower():
                return "Goodbye"
        
    i = classify(inp)
    if i:  # Checks whether the classification worked (If it didn't work, "i" would be "False")
        
        
        if (not 'context_filter' in i) or (userId in context and 'context_filter' in i and i['context_filter'] == context[userId]):  # Checking for context

            if 'context_set' in i:  # Checks whether the classification requires context to be set
                print('context:', i['context_set'])
                context[userId] = i['context_set']

            # Information extraction
            tree = prep_for_extract(inp)
            if i['tag']=="no signal":
                location = extract_info.low_signal_location(tree)
                if location:
                    #context[userId] = "no signal description"
                    return "We will look into the loss of signal in " + location + ". Thank you for staying with our network."
                else:
                    context[userId] = "no signal location"
                    while context[userId]!= "no signal location":
                        pass
                    return "Where did you face difficulties connecting to our network?"
            elif i['tag']=="change package":
                package = extract_info.package(tree)
                if package:
                    return "Okay, I'll change your package to " + package
                else:
                    context[userId] = "change package name"
                    while context[userId]!= "change package name":
                        pass
                    return "Which package do you want to change to? Context:" + context[userId]
            elif i['tag']=="new package":
                package = extract_info.package(tree)
                if package:
                    return "Okay, I'll activate " + package + " for you"
                else:
                    context[userId] = "new package name"
                    while context[userId]!= "new package name":
                        pass
                    return "Which package do you want to activate? Context:" + context[userId]

            responses = i["responses"]
            return random.choice(responses)
        else:  # The context didn't match
            return "I'm sorry, I didn't get that. Please try again. Context:" + context[userId]
    else:  # The classification didn't work
        return "I'm sorry, I didn't get that. Please try again. Context:" + context[userId]


#app.run(port=5000, debug=True)