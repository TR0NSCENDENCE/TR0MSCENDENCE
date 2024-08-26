from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from smtplib import SMTPException
import requests

def send_activation_mail(instance: User):
    subject = '[TR0NSCENDENCE][' + instance.username + '] Activation email'
    activation_url = settings.ORIGIN_HOSTNAME + '/activation/' + str(instance.activation_uuid)

    if settings.DEBUG:
        print('activate: ', activation_url)

    html_content = 'To activate your account, click <a href="' + activation_url +'">here</a> !'
    message = EmailMultiAlternatives(subject, 'To activate your account go to : ' + activation_url, None, [instance.email])
    message.attach_alternative(html_content, 'text/html')

    try:
        if not settings.DEBUG:
            message.send()
    except SMTPException:
        # Prevent account to be blocked
        instance.is_active = True
        instance.save()
        print('SMTP error (to_email:', instance.email, ')')


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        if not instance.is_active:
            send_activation_mail(instance)
    instance.user_profile.save()
