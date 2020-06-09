from unittest import TestCase
import telecomchatbot


class TestTelecomChatbot(TestCase):

    def test_classify(self):
        messages_greeting = ["Hi", "How are you", "Is anyone there?", "Hello", "Good day", "Whats up?"]
        for message in messages_greeting:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "greeting")

        messages_goodbye = ["See you later", "Goodbye", "Have a Good day", "bye"]
        for message in messages_goodbye:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "goodbye")

        messages_chatbot_functions = ["What can you do?", "Show me what you can do", "What are your functions"]
        for message in messages_chatbot_functions:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "chatbot functions")

        messages_no_signal = ["I am not getting signal", "There is no connection",
                              "My connection is gone", "There isn't any signal", "There is no signal",
                              "I have no signal", "I can't connect to the network", "Loss of signal",
                              "I am not getting any signal", "There is no signal in Colombo",
                              "I have no signal in Colombo", "I can't connect to the network in Colombo"]
        for message in messages_no_signal:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "no signal")

        messages_low_signal = ["I have low signal", "The connection is slow", "Internet is slow",
                               "Weak Signal", "The signal is weak", "Signal is poor", "Internet speeds are poor",
                               "The signal in weak in Colombo", "The internet speeds are poor in Colombo",
                               "The internet is slow in Colombo"]
        for message in messages_low_signal:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "low signal")

        messages_change_data_package = ["Can I change my data package", "I want a different data package",
                                        "I want to change my data package", "I want to change the data package",
                                        "Change data package", "Change my data package to",
                                        "I would like to change my data package"]
        for message in messages_change_data_package:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "change data package")

        messages_new_data_package = ["I want to activate a new data package", "I want to activate a data package",
                                     "I want a new data package", "Activate data package",
                                     "I want to activate a data package", "Can I activate a new data package?",
                                     "I want to activate the D99 data package", "Please activate the D99 data package"]
        for message in messages_new_data_package:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "new data package")

        messages_deactivate_data_package =["I want to deactivate my data package", "deactivate my data package",
                                           "I want to deactivate data package", "deactivate data package"]
        for message in messages_deactivate_data_package:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "deactivate data package")

        messages_change_voice_package = ["Can I change my voice package", "I want a different voice package",
                                         "I want to change my voice package", "I want to change the voice package",
                                         "Change voice package", "Change my voice package to",
                                         "I would like to change my voice package",
                                         "Please change my voice package V100", "change voice package V100"]
        for message in messages_change_voice_package:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "change voice package")

        messages_new_voice_package = ["I want to activate a new voice package", "I want to activate a voice package",
                                      "I want a new voice package", "Activate voice package",
                                      "I want to activate a voice package", "Can I activate a new voice package?",
                                      "I want to activate the V20 voice package", "Please activate V20 voice package"]
        for message in messages_new_voice_package:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "new voice package")

        messages_deactivate_voice_package = ["I want to deactivate my voice package", "deactivate my voice package",
                                             "I want to deactivate voice package", "deactivate voice package"]
        for message in messages_deactivate_voice_package:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "deactivate voice package")

        messages_data_usage_data = ["How much data have I used?", "How much data do I have left?",
                                    "How much data is remaining?", "View data usage", "I want to view my data usage",
                                    "What's my data usage?", "What is my data usage?",
                                    "Can you show me my data usage?", "data usage data",
                                    "Show me my data package usage", "Show me my data usage details.",
                                    "Show me data package usage details"]
        for message in messages_data_usage_data:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "data usage data")

        messages_voice_usage_data = ["How many minutes of voice calls have I used?",
                                     "How many minutes of voice calls do I have left?",
                                     "How many minutes are remaining?", "View voice usage",
                                     "I want to view my voice usage", "How many minutes do I have left?",
                                     "What is my voice usage?", "Can you show me my voice usage?",
                                     "voice usage data", "Show me my voice package usage",
                                     "Show me my voice package usage details", "Show me my voice usage details"]
        for message in messages_voice_usage_data:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "voice usage data")

        messages_usage_data = ["How much have I used?", "View usage", "I want to view my usage", "What's my usage?",
                               "What is my usage?", "Can you show me my usage?"]
        for message in messages_usage_data:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "usage data")

        messages_request_data_package_info = ["View data package info",
                                              "I'd like to know the details of data packages available",
                                              "I want to know the details of data packages available",
                                              "I want to know the data package details",
                                              "View data package information", "Show me details of data packages",
                                              "Details of data packages", "Show me data package details",
                                              "What are the available data packages?"]
        for message in messages_request_data_package_info:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "request data package info")

        messages_request_voice_package_info = ["View voice package info",
                                               "I'd like to know the details of voice packages available",
                                               "I want to know the details of voice packages available",
                                               "I want to know the voice package details",
                                               "View voice package information", "Show me details of voice packages",
                                               "Details of voice packages", "Show me voice package details",
                                               "What are the available voice packages?"]
        for message in messages_request_voice_package_info:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "request voice package info")

        messages_request_package_info = ["View D99 package info", "I'd like to know the details of the V200 package",
                                         "I'd like to know the details of the  package",
                                         "I want to know the details of the D49 package",
                                         "I want to know the details of the V100 package",
                                         "I want to know the  package details",
                                         "I want to know the D99 package details",
                                         "I want to know the details of data and voice packages",
                                         "Show me details of V100 package", "Details of V20 package",
                                         "What are the available packages?"]
        for message in messages_request_package_info:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "request package info")

        messages_thanks = ["Thank you", "Thanks"]
        for message in messages_thanks:
            self.assertEqual(telecomchatbot.classify(message)["tag"], "thanks")


