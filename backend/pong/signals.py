from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import GameInstance
from django.utils import timezone

@receiver(pre_save, sender=GameInstance)
def update_finish_data(sender, instance: GameInstance, **kwargs):
    if instance.state == 'FD':
        if not instance.finished_at:
            instance.finished_at = timezone.now()
