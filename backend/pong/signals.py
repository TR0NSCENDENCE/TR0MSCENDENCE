from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import GameInstance, TournamentInstance
from django.utils import timezone

@receiver(pre_save, sender=GameInstance)
def update_finish_data(sender, instance: GameInstance, **kwargs):
    if instance.state == 'FD':
        if not instance.finished_at:
            instance.finished_at = timezone.now()

@receiver(post_save, sender=TournamentInstance)
def create_halfs_match(sender, instance: TournamentInstance, created, **kwargs):
    if created:
        instance.gameinstance_half_1 = GameInstance.objects.create(player_one=instance.player_one, player_two=instance.player_two)
        instance.gameinstance_half_2 = GameInstance.objects.create(player_one=instance.player_thr, player_two=instance.player_fou)
        instance.gameinstance_half_1.save()
        instance.gameinstance_half_2.save()
        instance.save()
