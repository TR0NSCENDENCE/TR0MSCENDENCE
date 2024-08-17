from asgiref.sync import async_to_sync, sync_to_async
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

from users.models import User
from .models import GameInstance
from .game_state import GameState

class GameConsumer(AsyncJsonWebsocketConsumer):

    # Is this needed two times ?
    update_lock = asyncio.Lock()

    instances = {}

    update_lock = asyncio.Lock()

    async def connect(self):
        self.instance_uuid = self.scope["url_route"]["kwargs"]["instance_uuid"]
        self.instance_name = f"game_{self.instance_uuid}"
        self.user = self.scope["user"]

        # The instance exist ?
        try:
            self.instance = await GameInstance.objects.select_related('player_one', 'player_two').aget(uuid=self.instance_uuid)
        except GameInstance.DoesNotExist:
            # print(self.instance_uuid, 'instance not found')
            await self.close()
            return

        # The instance is in starting or in-game state
        if not self.instance.state in ['ST', 'IG']:
            # print(self.instance_uuid, 'match finished')
            await self.close()
            return

        # User is in the instance ?
        if not self.user in [self.instance.player_one, self.instance.player_two]:
            # print(self.user, 'not in the user of the instance')
            await self.close()
            return

        async with self.update_lock:
            if not self.instance_uuid in self.instances.keys():
                # print('instance created')
                self.instances[self.instance_uuid] = GameState(self.instance)
                asyncio.create_task(self.instances[self.instance_uuid].game_loop())
            try:
                self.instances[self.instance_uuid].player_connect(self.user, self)
            except self.GameState.AlreadyConnected:
                # print('user already connected to the instance')
                await self.close()
                return
        # Join room group and accept connection
        await self.channel_layer.group_add(self.instance_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if close_code == 1006:
            return
        # Leave room group
        await self.channel_layer.group_discard(self.instance_name, self.channel_name)
        # Disconnect from instance if exist
        async with self.update_lock:
            if self.instance_uuid in self.instances.keys():
                self.instances[self.instance_uuid].player_disconnect(self.user)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print("data receive : ", text_data)
        # Send message to room group
        await self.channel_layer.group_send(
            self.instance_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        print("message receive : ", event)
        # Send message to WebSocket
        await self.send(text_data="uho")

class MatchmakingConsumer(AsyncJsonWebsocketConsumer):

    waiting_list = {
        '1v1': [],
        'tournament': [],
    }

    users = []

    update_lock = asyncio.Lock()

    async def connect(self):
        self.match_type = self.scope["url_route"]["kwargs"]["match_type"]
        self.user = self.scope["user"]
        async with self.update_lock:
            if not self.match_type in self.waiting_list.keys():
                # print('unknown match type')
                await self.close()
                return
            if self.user in self.users:
                # print('user already in waiting list')
                await self.close()
                return
            self.users += [self.user]
            self.waiting_list[self.match_type] += [self]
        await self.accept()
        for key in self.waiting_list.keys():
            if len(self.waiting_list[key]) > 0 and not self.matchmaking_running[self.match_type]:
                # print('launch matchmaking for', self.match_type)
                asyncio.create_task(self.matchmaking_function[self.match_type](self))
                self.matchmaking_running[self.match_type] = True

    async def disconnect(self, close_code):
        if close_code == 1006:
            return
        async with self.update_lock:
            try:
                self.waiting_list[self.match_type].remove(self)
            except:
                pass
            try:
                self.users.remove(self.user)
            except:
                pass

    async def matchmaking_loop_1v1(self):
        async def create_match(consumers):
            new_instance = await sync_to_async(GameInstance.objects.create)(player_one=consumers[0].user, player_two=consumers[1].user)
            return new_instance.uuid

        while len(self.waiting_list['1v1']) > 0:
            async with self.update_lock:
                if len(self.waiting_list['1v1']) >= 2:
                    match_uuid = await create_match(self.waiting_list['1v1'][:2])
                    for c in [self.waiting_list['1v1'][0], self.waiting_list['1v1'][1]]:
                        await c.send_json({'type': 'found', 'uuid': str(match_uuid)})
                        await c.close()
                    self.waiting_list['1v1'] = self.waiting_list['1v1'][2:]
            await asyncio.sleep(0.5)
        self.matchmaking_running['1v1'] = False

    matchmaking_function = {
        '1v1': matchmaking_loop_1v1,
        'tournament': None,
    }

    matchmaking_running = {
        '1v1': False,
        'tournament': False,
    }
