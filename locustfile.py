from locust import HttpUser, TaskSet, task, between
import datetime
import json

SERVER_URL = "https://psichatbot-server.herokuapp.com"

USER_ID = 1

class FlowException(Exception):
    pass

class TestBehaviour(TaskSet):
    def on_start(self):
        global USER_ID 
        self.userId = USER_ID
        USER_ID +=1
    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    # @task(1)
    # def testGet(self):
    #     self.client.get("{}".format(SERVER_URL))

    @task(1)
    def chatbotRely(self):
        date_handler = lambda obj: (
            obj.isoformat()
            if isinstance(obj, (datetime.datetime, datetime.date))
            else None
        )

        ident = json.dumps(datetime.datetime.utcnow(), default=date_handler).strip('"')
        self.client.post("{}/telecom".format(SERVER_URL),json=
        {
            "id" : ident,
            "userId":self.userId,
            "message": "Hi",
            "context": "",
            "isBot": False
        })
    @task(1)
    def chatbotRelyUsageData(self):
        date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
        )
        ident = json.dumps(datetime.datetime.utcnow(), default=date_handler).strip('"')
        response =  self.client.post("{}/telecom".format(SERVER_URL),json=
                    {
                        "id" : ident,
                        "userId": self.userId,
                        "message": "Show me D99 package details",
                        "context": "",
                        "isBot": False
                    }, catch_response=True)

        print(response.text)
            # if response.text[4] != "Here are the details of the data package\n\nD99\nAvailable data:1000.0MB\nValid period:21days \nPrice: Rs. 99.0":
            #     raise FlowException("Request Failed")
    @task(3)
    def testLogin(self):
        self.client.post("{}/api/auth/login".format(SERVER_URL),json=
        {
            "email": "test@gmail.com",
            "password": "12345678"
        })

class WebsiteTest(HttpUser):
    tasks  = [TestBehaviour]
    wait_time = between(0.5, 3.0)