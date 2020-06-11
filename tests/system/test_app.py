from tests.system.mock_db import MockDB
import json
import datetime


class TestHome(MockDB):
    def test_testGet(self):
        with self.app() as c:
            resp = c.get('/')
            
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(
                json.loads(resp.get_data()),
                {"userId": 1,"isBot": True}
            )

    def test_greeting(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "Hello", "isBot": False,
                                               "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k:v for k,v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'userId':3,
                            'message':"Hi there, how can I help you?\n\nHere are some of the things I can do.\n1. Activate, Change or Deactivate data or voice packages.\n   Eg: I want to activate <package name> data package. I want to change my voice package. I want to deactivate my data package.\n\n2. Complain about the loss of signal or low signal.\n   Eg: There is no signal. I am not getting any signal. Internet is slow. The signal is weak.\n\n3. View usage data.\n   Eg: View data usage. How many minutes do I have left? Show me my voice package usage.\n\n4. View package information.\n   Eg: Show me the details of data packages. Show me the details of <package name> package. Show me the details of packages.\nYou may enter 'cancel' to exit out of any ongoing action.",
                            'context': ''}

                self.assertEqual(data, expected)

    def test_goodbye(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "See you later", "isBot": False,
                                               "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                
                self.assertEqual(data['context'], '')
                self.assertEqual(data['userId'], 3)
                self.assertIn(data['message'], ['Goodbye!', 'Talk to you later'])

    def test_chatbot_functions(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "What can you do?", "isBot": False,
                                               "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': "Here are some of the things I can do.\n1. Activate, Change or Deactivate data or voice packages.\n   Eg: I want to activate <package name> data package. I want to change my voice package. I want to deactivate my data package.\n\n2. Complain about the loss of signal or low signal.\n   Eg: There is no signal. I am not getting any signal. Internet is slow. The signal is weak.\n\n3. View usage data.\n   Eg: View data usage. How many minutes do I have left? Show me my voice package usage.\n\n4. View package information.\n   Eg: Show me the details of data packages. Show me the details of <package name> package. Show me the details of packages.\nYou may enter 'cancel' to exit out of any ongoing action.",
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_no_signal(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "I am not getting signal",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'no signal location',
                            'message': 'Where did you face difficulties connecting to our network?',
                            'userId': 3}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 3, "id": ident, "message": "Colombo", "isBot": False,
                                   "context": "no signal location"}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'We will look into the loss of signal in Colombo. Thank you for staying with our network.',
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_no_signal_with_location(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "I have no signal in Colombo",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'We will look into the loss of signal in Colombo. Thank you for staying with our network.',
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_low_signal(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "I have low signal",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'low signal location',
                            'message': 'Where did you face difficulties connecting to our network?',
                            'userId': 3}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 3, "id": ident, "message": "Colombo", "isBot": False,
                                   "context": "low signal location"}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'We will look into the weak signal in Colombo. Thank you for staying with our network.',
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_low_signal_with_location(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "The signal is weak in Colombo",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'We will look into the weak signal in Colombo. Thank you for staying with our network.',
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_change_data_package(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 1, "id": ident, "message": "Can I change my data package",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'change data package name',
                            'message': 'Which data package do you want to change to? \nD29-(200.0MB, 2days)\nD49-(400.0MB, 7days)\nD99-(1000.0MB, 21days)\nD199-(2000.0MB, 30days)\nD349-(4000.0MB, 30days)\nD499-(6000.0MB, 30days)\nD649-(8500.0MB, 30days)\n',
                            'userId': 1}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 1, "id": ident, "message": "D99",
                                               "isBot": False, "context": "change data package name"}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Your data package has been successfully changed to D99. You now have 1000.0MB remaining.',
                            'userId': 1}
                
                self.assertEqual(data, expected)

    def test_change_data_package_with_name(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 1, "id": ident, "message": "I want to change my data package D99",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Your data package has been successfully changed to D99. You now have 1000.0MB remaining.',
                            'userId': 1}

                self.assertEqual(data, expected)

    def test_change_voice_package(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 1, "id": ident, "message": "Can I change my voice package",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'change voice package name',
                            'message': 'Which voice package do you want to change to? \nV20-(30.0minutes, 7days)\nV60-(100.0minutes, 7days)\nV100-(200.0minutes, 14days)\nV200-(400.0minutes, 30days)\n',
                            'userId': 1}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 1, "id": ident, "message": "V100",
                                               "isBot": False, "context": "change voice package name"}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Your voice package has been successfully changed to V100. You now have 200.0 minutes remaining.',
                            'userId': 1}

                self.assertEqual(data, expected)

    def test_change_voice_package_with_name(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 1, "id": ident, "message": "I want to change my voice package V100",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Your voice package has been successfully changed to V100. You now have 200.0 minutes remaining.',
                            'userId': 1}

                self.assertEqual(data, expected)

    def test_new_data_package(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "I want to activate a new data package",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'new data package name',
                            'message': 'Which data package do you want to activate? \nD29-(200.0MB, 2days)\nD49-(400.0MB, 7days)\nD99-(1000.0MB, 21days)\nD199-(2000.0MB, 30days)\nD349-(4000.0MB, 30days)\nD499-(6000.0MB, 30days)\nD649-(8500.0MB, 30days)\n',
                            'userId': 3}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "D99",
                                               "isBot": False, "context": "new data package name"}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'D99 package has been successfully activated. You now have 1000.0MB remaining',
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_new_data_package_with_name(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 4, "id": ident, "message": "I want to activate the D99 data package",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'D99 package has been successfully activated. You now have 1000.0MB remaining',
                            'userId': 4}

                self.assertEqual(data, expected)

    def test_new_voice_package(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "I want to activate a new voice package",
                                               "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'new voice package name',
                            'message': 'Which voice package do you want to activate? \nV20-(30minutes, 7days)\nV60-(100minutes, 7days)\nV100-(200minutes, 14days)\nV200-(400minutes, 30days)\n',
                            'userId': 3}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps({"userId": 3, "id": ident, "message": "V100",
                                               "isBot": False, "context": "new voice package name"}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'V100 package has been successfully activated. You now have 200.0 minutes remaining.',
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_new_voice_package_with_name(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 4, "id": ident, "message": "I want to activate the V100 voice package",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'V100 package has been successfully activated. You now have 200.0 minutes remaining.',
                            'userId': 4}

                self.assertEqual(data, expected)

    def test_deactivate_data_package(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 3, "id": ident, "message": "I want to activate the D99 data package",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 3, "id": ident, "message": "I want to deactivate my data package",
                                   "isBot": False, "context": ""}),
                                  content_type='application/json'
                              )

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'deactivate data package',
                            'message': 'Are you sure you want to deactivate your data package?',
                            'userId': 3}
                
                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 3, "id": ident, "message": "Yes",
                                   "isBot": False, "context": "deactivate data package"}),
                              content_type='application/json'
                              )

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Your data package has been successfully deactivated.',
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_deactivate_voice_package(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 3, "id": ident, "message": "I want to activate the V100 voice package",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 3, "id": ident, "message": "I want to deactivate my voice package",
                                   "isBot": False, "context": ""}),
                              content_type='application/json'
                              )

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'deactivate voice package',
                            'message': 'Are you sure you want to deactivate your voice package?',
                            'userId': 3}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 3, "id": ident, "message": "Yes",
                                   "isBot": False, "context": "deactivate voice package"}),
                              content_type='application/json'
                              )

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Your voice package has been successfully deactivated.',
                            'userId': 3}

                self.assertEqual(data, expected)

    def test_deactivate_package(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 4, "id": ident, "message": "I want to activate the D99 data package",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 4, "id": ident, "message": "I want to deactivate my package",
                                   "isBot": False, "context": ""}),
                              content_type='application/json'
                              )

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'deactivate package',
                            'message': 'Which package do you want to deactivate? Voice or Data?',
                            'userId': 4}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 4, "id": ident, "message": "Data",
                                   "isBot": False, "context": "deactivate package"}),
                              content_type='application/json'
                              )

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': 'deactivate data package',
                            'message': 'Are you sure you want to deactivate your data package?',
                            'userId': 4}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 4, "id": ident, "message": "Yes",
                                   "isBot": False, "context": "deactivate data package"}),
                              content_type='application/json'
                              )

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Your data package has been successfully deactivated.',
                            'userId': 4}

                self.assertEqual(data, expected)

    def test_data_usage_data(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 2, "id": ident, "message": "How much data have I used?",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Active data package: D499\nRemaining data: 6000.0MB\nRemaining days: 29 days 24 hours 60 minutes',
                            'userId': 2}
                
                self.assertEqual(data, expected)

    def test_voice_usage_data(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 2, "id": ident, "message": "How many minutes of voice calls have I used?",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Active voice package: V200\nRemaining talk time: 400 minutes\nRemaining days: 29 days 24 hours 60 minutes',
                            'userId': 2}

                self.assertEqual(data, expected)

    def test_usage_data(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 2, "id": ident, "message": "How much have I used?",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Data package usage\n----------------------------------\nActive data package: D499\nRemaining data: 6000.0MB\nRemaining days: 29 days 24 hours 60 minutes\n\nVoice package usage\n-----------------------------------\nActive voice package: V200\nRemaining talk time: 400 minutes\nRemaining days: 29 days 24 hours 60 minutes',
                            'userId': 2}

                self.assertEqual(data, expected)

    def test_request_data_package_info(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 2, "id": ident, "message": "View data package info",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Here are the available data packages. \n\nD29-(200.0MB, 2days, Rs. 29.0 )\nD49-(400.0MB, 7days, Rs. 49.0 )\nD99-(1000.0MB, 21days, Rs. 99.0 )\nD199-(2000.0MB, 30days, Rs. 199.0 )\nD349-(4000.0MB, 30days, Rs. 349.0 )\nD499-(6000.0MB, 30days, Rs. 499.0 )\nD649-(8500.0MB, 30days, Rs. 649.0 )\n',
                            'userId': 2}

                self.assertEqual(data, expected)

    def test_request_voice_package_info(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 2, "id": ident, "message": "View voice package info",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Here are the available voice packages. \n\nV20-(30minutes, 7days, Rs. 20.0 )\nV60-(100minutes, 7days, Rs. 60.0 )\nV100-(200minutes, 14days, Rs. 100.0 )\nV200-(400minutes, 30days, Rs. 200.0 )\n',
                            'userId': 2}

                self.assertEqual(data, expected)

    def test_request_package_info(self):
        with self.app() as c:
            with self.mock_db_config:
                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 2, "id": ident, "message": "What are the available packages?",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Here are all the available package\n\nHere are the available data packages. \n\nD29-(200.0MB, 2days, Rs. 29.0 )\nD49-(400.0MB, 7days, Rs. 49.0 )\nD99-(1000.0MB, 21days, Rs. 99.0 )\nD199-(2000.0MB, 30days, Rs. 199.0 )\nD349-(4000.0MB, 30days, Rs. 349.0 )\nD499-(6000.0MB, 30days, Rs. 499.0 )\nD649-(8500.0MB, 30days, Rs. 649.0 )\n\n\nHere are the available voice packages. \n\nV20-(30minutes, 7days, Rs. 20.0 )\nV60-(100minutes, 7days, Rs. 60.0 )\nV100-(200minutes, 14days, Rs. 100.0 )\nV200-(400minutes, 30days, Rs. 200.0 )\n',
                            'userId': 2}

                self.assertEqual(data, expected)

                ident = get_ident()

                resp = c.post('/telecom',
                              data=json.dumps(
                                  {"userId": 2, "id": ident,
                                   "message": "I'd like to know the details of the V200 package",
                                   "isBot": False, "context": ""}),
                              content_type='application/json')

                self.assertEqual(resp.status_code, 200)

                data = json.loads(resp.get_data())
                data = {k: v for k, v in data.items() if k in ['userId', 'message', 'context']}

                expected = {'context': '',
                            'message': 'Here are the details of the voice package\n\nV200\nAvailable talktime:400minutes\nValid period: 30days\nPrice: Rs. 200.0',
                            'userId': 2}

                self.assertEqual(data, expected)


def get_ident():
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    ident = json.dumps(datetime.datetime.utcnow(), default=date_handler).strip('"')
    return ident
