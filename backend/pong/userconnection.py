from users.models import User

class UserConnection():
    class AlreadyConnected(Exception):
        pass

    def __init__(self):
        self.connected = False
        self.consumer = None
        self.user = None
    
    def connect(self, user: User, consumer):
        if self.connected:
            raise self.AlreadyConnected
        self.consumer = consumer
        self.user = user
        self.connected = True

    def disconnect(self):
        self.connected = False
        self.consumer = None

    async def send_json(self, json_data):
        if self.connected:
            await self.consumer.send_json(json_data)
