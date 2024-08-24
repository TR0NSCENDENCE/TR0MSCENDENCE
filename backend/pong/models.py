from django.db import models
from uuid import uuid4
from users.models import User
from django.utils.translation import gettext_lazy as _

class GameInstance(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    class GameState(models.TextChoices):
        STARTING = "ST", _('Starting')
        INGAME = 'IG', _('In-Game')
        FINISHED = 'FD', _('Finished')
    state = models.CharField(
        max_length=2,
        choices=GameState,
        default=GameState.STARTING
    )
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gameinstance_winner", null=True, default=None, blank=True)
    player_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gameinstance_player_one")
    player_one_score = models.PositiveIntegerField(default=0)
    player_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gameinstance_player_two")
    player_two_score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True, default=None)

    def tournament_uuid(self):
        try:
            return self.tournament_1.uuid
        except:
            pass
        try:
            return self.tournament_2.uuid
        except:
            pass
        try:
            return self.tournament_3.uuid
        except:
            pass
        return None

    def __str__(self):
        return f"GAME INSTANCE {self.player_one.get_username()} vs {self.player_two.get_username()} (uuid: {self.uuid})"

class TournamentInstance(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    finished_at = models.DateTimeField(null=True, blank=True, default=None)

    class TournamentState(models.TextChoices):
        WAITING_PLAYERS = 'WP', _('Waiting for players')
        INGAME_HALF = 'IH', _('In-Game half')
        INGAME_FINAL = 'IF', _('In-Game final')
        FINISHED = 'FD', _('Finished')
    state = models.CharField(
        max_length=2,
        choices=TournamentState,
        default=TournamentState.WAITING_PLAYERS
    )

    gameinstance_half_1 = models.OneToOneField(GameInstance, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='tournament_1')
    winner_half_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_winner_half_1", null=True, default=None, blank=True)

    gameinstance_half_2 = models.OneToOneField(GameInstance, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='tournament_2')
    winner_half_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_winner_half_2", null=True, default=None, blank=True)

    gameinstance_final = models.OneToOneField(GameInstance, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='tournament_3')
    winner_final = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_winner_final", null=True, default=None, blank=True)

    player_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_player_one")
    player_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_player_two")
    player_thr = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_player_thr")
    player_fou = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournament_player_fou")

    def create_match_half_1(self):
        self.gameinstance_half_1 = GameInstance.objects.create(player_one=self.player_one, player_two=self.player_two)
        self.save()

    def create_match_half_2(self):
        self.gameinstance_half_2 = GameInstance.objects.create(player_one=self.player_thr, player_two=self.player_fou)
        self.save()

    def create_match_final(self):
        self.gameinstance_final = GameInstance.objects.create(player_one=self.winner_half_1, player_two=self.winner_half_2)

    def __str__(self):
        return f"TOURNAMENT INSTANCE (uuid: {self.uuid})"
