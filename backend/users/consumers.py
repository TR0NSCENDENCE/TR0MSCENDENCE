from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class OnlineTracker(AsyncWebsocketConsumer):

    users = {}

    @database_sync_to_async
    def update_online_status(self, is_online):
        str_user_id = str(self.user.pk)
        if str_user_id in self.users.keys():
            self.users[str_user_id] += 1 if is_online else -1
        else:
            self.users[str_user_id] = 1
        _is_online = self.users[str_user_id] >= 1
        self.user.user_profile.online_status = _is_online
        # print(self.user, 'online status', _is_online, 'counter', self.users[str_user_id])
        self.user.user_profile.save()

    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        await self.update_online_status(True)

    async def disconnect(self, close_code):
        await self.update_online_status(False)
