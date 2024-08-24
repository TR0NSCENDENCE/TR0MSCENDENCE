import asyncio
import json
from asgiref.sync import async_to_sync, sync_to_async
from users.models import User
from autobahn.exception import Disconnected
from datetime import datetime, timedelta
from functools import reduce

from .userconnection import UserConnection
from .models import GameInstance, TournamentInstance
from .serializers import TournamentInstanceInfoSerializer

CLOSE_CODE_ERROR = 3000
CLOSE_CODE_OK = 3001

class TournamentState():

    # Fields:
    #   instance: TournamentInstance
    #   players: UserConnectionc
    #   half_1_timeout: bool
    #   half_2_timeout: bool
    #   final_timeout: bool


    def __init__(self, instance: TournamentInstance):
        self.instance = instance
        self.player_connections = [UserConnection() for _i in range(4)]
        self.half_1_timeout = False
        self.half_2_timeout = False
        self.final_timeout = False

    def player_connect(self, user: User, consumer):
        if self.instance.player_one == user:
            self.log(user, 'player_one')
            self.player_connections[0].connect(user, consumer)
        if self.instance.player_two == user:
            self.log(user, 'player_two')
            self.player_connections[1].connect(user, consumer)
        if self.instance.player_thr == user:
            self.log(user, 'player_thr')
            self.player_connections[2].connect(user, consumer)
        if self.instance.player_fou == user:
            self.log(user, 'player_fou')
            self.player_connections[3].connect(user, consumer)

    def player_disconnect(self, player: User):
        if self.instance.player_one == player:
            self.player_connections[0].disconnect()
        if self.instance.player_two == player:
            self.player_connections[1].disconnect()
        if self.instance.player_thr == player:
            self.player_connections[2].disconnect()
        if self.instance.player_fou == player:
            self.player_connections[3].disconnect()

    async def player_receive_json(self, consumer, json_data):
        pass

    async def players_send_json(self, data):
        for player_connection in self.player_connections:
            try:
                await player_connection.send_json(data)
            except Disconnected:
                pass

    #==========================================================================#
    # Utils
    #==========================================================================#

    def players_connected(self):
        return reduce(lambda a, b: a and b, [c.connected for c in self.player_connections])

    def instance_finished(self):
        self.log('Tournament finished !')
        self.instance.state = 'FD'
        self.instance.save()

    async def close_consumers(self, close_code=None):
        for uc in self.player_connections:
            if uc.connected:
                uc.consumer.close(close_code)
                uc.disconnect()

    def get_half_matchs(self):
        # To load from db in sync context
        self.instance.gameinstance_half_1.player_one
        self.instance.gameinstance_half_1.player_two
        self.instance.gameinstance_half_2.player_one
        self.instance.gameinstance_half_2.player_two
        return [self.instance.gameinstance_half_1, self.instance.gameinstance_half_2]

    async def half_refresh_from_db(self):
        await self.instance.gameinstance_half_1.arefresh_from_db()
        await self.instance.gameinstance_half_2.arefresh_from_db()

    async def final_refresh_from_db(self):
        await self.instance.gameinstance_final.arefresh_from_db()

    async def instance_refresh_from_db(self):
        await self.instance.arefresh_from_db(from_queryset=TournamentInstance.objects.select_related('player_one', 'player_two', 'player_thr', 'player_fou'))

    async def instance_set_state(self, state):
        self.instance.state = state
        await sync_to_async(self.instance.save)()

    def get_tournament_instance_data(self):
        return TournamentInstanceInfoSerializer(self.instance).data

    def create_final(self):
        self.instance.create_match_final()
        self.instance.save()

    async def update_tournamentstate_consumers(self):
        await self.players_send_json({
            'type': 'tournament_update',
            'tournament_data': await sync_to_async(self.get_tournament_instance_data)()
        })

    #==========================================================================#
    # Pure game logic
    #==========================================================================#

    def log(self, *args):
        RED = '\033[0;31m'
        BLUE = '\033[0;34m'
        RESET = '\033[0m'
        message = f'{RED}[{BLUE}TI#{self.instance.uuid}{RED}]{RESET}'
        print(message, *args)

    async def start_halfs(self):
        await self.instance_set_state('IH')
        for game_instance in await sync_to_async(self.get_half_matchs)():
            for uc in self.player_connections:
                if uc.user in [game_instance.player_one, game_instance.player_two]:
                    await uc.send_json({
                        'type': 'match_start',
                        'match_uuid': str(game_instance.uuid)
                    })

    async def start_final(self):
        await self.instance_set_state('IF')
        for uc in self.player_connections:
            if uc.user in [self.instance.gameinstance_final.player_one, self.instance.gameinstance_final.player_two]:
                await uc.send_json({
                    'type': 'match_start',
                    'match_uuid': str(self.instance.gameinstance_final.uuid)
                })

    MATCH_START_TIMEOUT = 20

    async def wait_for_halfs(self):
        t_start = datetime.now()
        while self.instance.gameinstance_half_1.state != 'FD' or self.instance.gameinstance_half_2.state != 'FD':
            if datetime.now() - t_start > timedelta(seconds=self.MATCH_START_TIMEOUT):
                if self.instance.gameinstance_half_1.state == 'ST' \
                        and self.instance.gameinstance_half_2.state == 'ST':
                    self.half_1_timeout = True
                    self.half_2_timeout = True
                    break
                elif self.instance.gameinstance_half_1.state == 'ST' \
                        and self.instance.gameinstance_half_2.state == 'FD':
                    self.half_1_timeout = True
                    self.log(self.instance.gameinstance_half_1.uuid, 'match timeout')
                    break
                elif self.instance.gameinstance_half_2.state == 'ST' \
                        and self.instance.gameinstance_half_1.state == 'FD':
                    self.half_2_timeout = True
                    self.log(self.instance.gameinstance_half_2.uuid, 'match timeout')
                    break
            await asyncio.sleep(1.)
            await self.half_refresh_from_db()
            await self.instance_refresh_from_db()
            await self.update_tournamentstate_consumers()
            # self.log('Waiting for matchs to finish...')

    async def wait_for_players(self):
        self.log("Waiting for player to connect...")
        while not self.players_connected():
            await asyncio.sleep(1. / 10)

    async def wait_for_winners(self):
        winners = []
        for uc in self.player_connections:
            if uc.user == self.instance.winner_half_1 or uc.user == self.instance.winner_half_2:
                winners += [uc]
        assert(len(winners) == 2)
        while not winners[0].connected or not winners[1].connected:
            await asyncio.sleep(1.)
            await self.half_refresh_from_db()
            await self.instance_refresh_from_db()
            await self.update_tournamentstate_consumers()
            # self.log("Waiting for winners to connect...")

    async def wait_for_final(self):
        while self.instance.gameinstance_final.state != 'FD':
            await asyncio.sleep(1.)
            await self.final_refresh_from_db()
            await self.instance_refresh_from_db()
            await self.update_tournamentstate_consumers()
            # self.log('Waiting for final to finish...')

    async def tournament_loop(self):
        await self.wait_for_players()
        await self.start_halfs()
        await self.wait_for_halfs()
        if self.half_1_timeout and self.half_2_timeout:
            self.log('2 halfs timeout...')
            await self.close_consumers(CLOSE_CODE_OK)
            return
        elif self.half_1_timeout or self.half_2_timeout:
            self.instance.winner_final = await sync_to_async(lambda: self.instance.gameinstance_half_2.winner if self.half_1_timeout else self.instance.gameinstance_half_1.winner)()
            await sync_to_async(self.instance.save)()
            await self.update_tournamentstate_consumers()
            await self.close_consumers(CLOSE_CODE_OK)
            return
        await sync_to_async(self.create_final)()
        await self.wait_for_winners()
        await self.start_final()
        await self.wait_for_final()
        self.log('TOURNAMENT FINISHED')
        await self.instance_set_state('FD')
        await self.close_consumers(CLOSE_CODE_OK)
