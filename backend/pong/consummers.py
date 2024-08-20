from asgiref.sync import async_to_sync, sync_to_async
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

from users.models import User
from .models import GameInstance, TournamentInstance
from .game_state import GameState

class GameConsumer(AsyncJsonWebsocketConsumer):

    game_states = {}

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
            if not self.instance_uuid in self.game_states.keys():
                # print('instance created')
                self.game_states[self.instance_uuid] = GameState(self.instance)
                asyncio.create_task(self.game_states[self.instance_uuid].game_loop())
            try:
                self.game_states[self.instance_uuid].player_connect(self.user, self)
                self.game_state = self.game_states[self.instance_uuid]
            except GameState.AlreadyConnected:
                print('user already connected to the instance')
                await self.close()
                return
        # Accept connection
        await self.accept()

    async def disconnect(self, close_code):
        if close_code == 1006:
            return
        # Disconnect from instance if exist
        async with self.update_lock:
            if self.instance_uuid in self.game_states.keys():
                self.game_states[self.instance_uuid].player_disconnect(self.user)

    # Receive message from WebSocket
    async def receive_json(self, json_data):
        await self.game_state.player_receive_json(self, json_data)

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
                    for c in self.waiting_list['1v1'][:2]:
                        await c.send_json({'type': 'found', 'uuid': str(match_uuid)})
                        await c.close()
                    self.waiting_list['1v1'] = self.waiting_list['1v1'][2:]
            await asyncio.sleep(0.5)
        self.matchmaking_running['1v1'] = False

    async def matchmaking_loop_tournament(self):
        async def create_tournament(consumers):
            new_instance = await sync_to_async(TournamentInstance.objects.create)(
                player_one=consumers[0].user,
                player_two=consumers[1].user,
                player_thr=consumers[2].user,
                player_fou=consumers[3].user
                )
            return new_instance.uuid

        while len(self.waiting_list['tournament']) > 0:
            async with self.update_lock:
                if len(self.waiting_list['tournament']) >= 4:
                    match_uuid = await create_match(self.waiting_list['tournament'][:4])
                    for c in self.waiting_list['tournament'][:4]:
                        await c.send_json({'type': 'found', 'uuid': str(match_uuid)})
                        await c.close()
                    self.waiting_list['tournament'] = self.waiting_list['tournament'][4:]
            await asyncio.sleep(0.5)
        self.matchmaking_running['tournament'] = False

    matchmaking_function = {
        '1v1': matchmaking_loop_1v1,
        'tournament': matchmaking_loop_tournament,
    }

    matchmaking_running = {
        '1v1': False,
        'tournament': False,
    }
