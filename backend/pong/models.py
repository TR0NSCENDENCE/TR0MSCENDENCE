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
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True, default=None, blank=True)
    player_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_one")
    player_one_score = models.PositiveIntegerField(default=0)
    player_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_two")
    player_two_score = models.PositiveIntegerField(default=0)
    score = models.Field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GAME INSTANCE {self.player_one.get_username()} vs {self.player_two.get_username()} (uuid: {self.uuid})"
