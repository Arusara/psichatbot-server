import chatbot_functions
from tests.integration.mock_db import MockDB
from mock import patch
from nltk.tree import *


class TestChatbotFunctions(MockDB):

    def test_no_signal(self):
        with self.mock_db_config:
            tree = Tree('S', [('There', 'EX'), ('is', 'VBZ'), ('no', 'DT'), ('signal', 'NN'), ('in', 'IN'),
                              Tree('GPE', [('Colombo', 'NNP')])])
            self.assertEqual(chatbot_functions.no_signal(tree, 1, "")[0],
                             "We will look into the loss of signal in Colombo. Thank you for staying with our network.")
            tree = Tree('S', [('There', 'EX'), ('is', 'VBZ'), ('no', 'DT'), ('signal', 'NN')])
            self.assertEqual(chatbot_functions.no_signal(tree, 1, "")[0],
                             "Where did you face difficulties connecting to our network?")

    def test_no_signal_location(self):
        with self.mock_db_config:
            tree = Tree('S', [Tree('GPE', [('Colombo', 'NN')])])
            self.assertEqual(chatbot_functions.no_signal_location(tree, 1, "no signal location")[0],
                             "We will look into the loss of signal in Colombo. Thank you for staying with our network.")
            tree= Tree('S', [('sentence', 'NN'), ('with', 'IN'), ('no', 'DT'), ('location', 'NN')])
            self.assertEqual(chatbot_functions.no_signal_location(tree, 1, "no signal location")[0],
                             "Please restate where you faced difficulties connecting to our network")

    def test_low_signal(self):
        with self.mock_db_config:
            tree = Tree('S', [('The', 'DT'), ('signal', 'NN'), ('is', 'VBZ'), ('weak', 'JJ'), ('in', 'IN'), Tree('GPE', [('Kandy', 'NNP')])])
            self.assertEqual(chatbot_functions.low_signal(tree, 1, "")[0],
                             "We will look into the weak signal in Kandy. Thank you for staying with our network.")
            tree = Tree('S', [('The', 'DT'), ('signal', 'NN'), ('is', 'VBZ'), ('weak', 'JJ'), ('.', '.')])
            self.assertEqual(chatbot_functions.low_signal(tree, 1, "")[0],
                             "Where did you face difficulties connecting to our network?")

    def test_low_signal_location(self):
        with self.mock_db_config:
            tree = Tree('S', [Tree('GPE', [('Kandy', 'NN')])])
            self.assertEqual(chatbot_functions.low_signal_location(tree, 1 , "low signal location")[0],
                             "We will look into the weak signal in Kandy. Thank you for staying with our network.")
            tree = Tree('S', [('sentence', 'NN'), ('with', 'IN'), ('no', 'DT'), ('location', 'NN')])
            self.assertEqual(chatbot_functions.low_signal_location(tree, 1, "low signal location")[0],
                             "Please restate where you faced difficulties connecting to our network")

    def test_change_data_package_function(self):
        with self.mock_db_config:
            tree = Tree('S',
                        [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('change', 'VB'),
                         ('my', 'PRP$'), ('data', 'NNS'), ('package', 'NN'), ('D99', 'NNP')])
            self.assertEqual(chatbot_functions.change_data_package_function(tree, "", 1)[0],
                             "Your data package has been successfully changed to D99. You now have 1000.0MB remaining.")
            tree = Tree('S',
                        [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('change', 'VB'),
                         ('my', 'PRP$'), ('data', 'NNS'), ('package', 'NN')])
            self.assertEqual(chatbot_functions.change_data_package_function(tree, "", 1)[0],
                             "Which data package do you want to change to? \n" +
                             "D29-(200.0MB, 2days)\nD49-(400.0MB, 7days)\nD99-(1000.0MB, 21days)\n" +
                             "D199-(2000.0MB, 30days)\nD349-(4000.0MB, 30days)\nD499-(6000.0MB, 30days)\n" +
                             "D649-(8500.0MB, 30days)\n")

    def test_change_data_package_name(self):
        with self.mock_db_config:
            tree = Tree('S', [Tree('GPE', [('D99', 'NN')])])
            self.assertEqual(chatbot_functions.change_data_package_name(tree, "", 1)[0],
                             "Your data package has been successfully changed to D99. You now have 1000.0MB remaining.")
            tree = Tree('S', [Tree('GPE', [('D150', 'NN')])])
            self.assertEqual(chatbot_functions.change_data_package_name(tree, "", 1)[0],
                             "I'm sorry but that's not a valid data package. These are the available data packages \n" +
                             "D29-(200.0MB, 2days)\nD49-(400.0MB, 7days)\nD99-(1000.0MB, 21days)\n" +
                             "D199-(2000.0MB, 30days)\nD349-(4000.0MB, 30days)\nD499-(6000.0MB, 30days)\n" +
                             "D649-(8500.0MB, 30days)\n"
                             )
            tree = Tree('S', [('no', 'DT'), ('package', 'NN'), ('name', 'NN')])
            self.assertEqual(chatbot_functions.change_data_package_name(tree, "", 1)[0],
                             "I'm sorry but that's not a valid data package name. Please try again. " +
                             "These are the available data packages \n" +
                             "D29-(200.0MB, 2days)\nD49-(400.0MB, 7days)\nD99-(1000.0MB, 21days)\n" +
                             "D199-(2000.0MB, 30days)\nD349-(4000.0MB, 30days)\nD499-(6000.0MB, 30days)\n" +
                             "D649-(8500.0MB, 30days)\n"
                             )

    def test_change_voice_package_function(self):
        with self.mock_db_config:
            tree = Tree('S',
                        [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('change', 'VB'), ('my', 'PRP$'), ('voice', 'NNS'),
                         ('package', 'NN'), ('V100', 'NNP')])
            self.assertEqual(chatbot_functions.change_voice_package_function(tree, "", 1)[0],
                             "Your voice package has been successfully changed to V100. " +
                             "You now have 200.0 minutes remaining.")
            tree = Tree('S',
                        [('I', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('change', 'VB'), ('my', 'PRP$'), ('voice', 'NNS'),
                         ('package', 'NN')])
            self.assertEqual(chatbot_functions.change_voice_package_function(tree, "", 1)[0],
                             "Which voice package do you want to change to? \n" +
                             "V20-(30.0minutes, 7days)\nV60-(100.0minutes, 7days)\n" +
                             "V100-(200.0minutes, 14days)\nV200-(400.0minutes, 30days)\n")

    def test_change_voice_package_name(self):
        with self.mock_db_config:
            tree = Tree('S', [Tree('GPE', [('V100', 'NN')])])
            self.assertEqual(chatbot_functions.change_voice_package_name(tree, "", 1)[0],
                             "Your voice package has been successfully changed to V100. " +
                             "You now have 200.0 minutes remaining.")
            tree = Tree('S', [Tree('GPE', [('V150', 'NN')])])
            self.assertEqual(chatbot_functions.change_voice_package_name(tree, "", 1)[0],
                             "I'm sorry but that's not a valid voice package. " +
                             "These are the available voice packages \n" +
                             "V20-(30.0minutes, 7days)\nV60-(100.0minutes, 7days)\n" +
                             "V100-(200.0minutes, 14days)\nV200-(400.0minutes, 30days)\n")
            tree = Tree('S', [('no', 'DT'), ('package', 'NN'), ('name', 'NN')])
            self.assertEqual(chatbot_functions.change_voice_package_name(tree, "", 1)[0],
                             "I'm sorry but that's not a valid voice package name. Please try again. " +
                             "These are the available voice packages \n" +
                             "V20-(30.0minutes, 7days)\nV60-(100.0minutes, 7days)\n" +
                             "V100-(200.0minutes, 14days)\nV200-(400.0minutes, 30days)\n")

    def test_new_data_package(self):
        with self.mock_db_config:
            tree = Tree('S', [('activate', 'NN'), ('D99', 'NNP'), ('data', 'NN'), ('package', 'NN')])
            self.assertEqual(chatbot_functions.new_data_package(tree, "", 3)[0],
                             "D99 package has been successfully activated. You now have 1000.0MB remaining")
            tree = Tree('S', [('activate', 'NN'), ('D150', 'NNP'), ('data', 'NN'), ('package', 'NN')])
            self.assertEqual(chatbot_functions.new_data_package(tree, "", 4)[0],
                             "I'm sorry but that's not a valid data package. These are the available data packages \n" +
                             "D29-(200.0MB, 2days)\nD49-(400.0MB, 7days)\nD99-(1000.0MB, 21days)\n" +
                             "D199-(2000.0MB, 30days)\nD349-(4000.0MB, 30days)\nD499-(6000.0MB, 30days)\n" +
                             "D649-(8500.0MB, 30days)\n"
                             )
            tree = Tree('S', [('activate', 'NN'), ('data', 'NNS'), ('package', 'NN')])
            self.assertEqual(chatbot_functions.new_data_package(tree, "", 5)[0],
                             "Which data package do you want to activate? \n" +
                             "D29-(200.0MB, 2days)\nD49-(400.0MB, 7days)\nD99-(1000.0MB, 21days)\n" +
                             "D199-(2000.0MB, 30days)\nD349-(4000.0MB, 30days)\nD499-(6000.0MB, 30days)\n" +
                             "D649-(8500.0MB, 30days)\n"
                             )

    # def test_new_data_package_name(self):
    #     with self.mock_db_config:




    def test_deactivate_data_confirmation(self):
        with self.mock_db_config:
            self.assertEqual(chatbot_functions.deactivate_data_confirmation("yes", 1, "deactivate data package")[0],
                             "Your data package has been successfully deactivated.")
            self.assertEqual(chatbot_functions.deactivate_data_confirmation("no", 1, "deactivate data package")[0],
                             "Okay. Is there anything else I can help you with?")
            self.assertEqual(chatbot_functions.deactivate_data_confirmation("something else", 1, "deactivate data package")[0],
                             "I'm sorry I didn't get that. Please answer with yes or no.")

    def test_deactivate_voice_confirmation(self):
        with self.mock_db_config:
            self.assertEqual(chatbot_functions.deactivate_voice_confirmation("yes", 1, "deactivate voice package")[0],
                             "Your voice package has been successfully deactivated.")
            self.assertEqual(chatbot_functions.deactivate_voice_confirmation("no", 1, "deactivate voice package")[0],
                             "Okay. Is there anything else I can help you with?")
            self.assertEqual(chatbot_functions.deactivate_voice_confirmation("something else", 1, "deactivate voice package")[0],
                             "I'm sorry I didn't get that. Please answer with yes or no.")

