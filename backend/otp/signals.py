from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from .models import OTPInstance
from django.core.mail import EmailMultiAlternatives
from users.models import User

def send_otp_mail(otpinstance: OTPInstance):
    subject = '[TR0NSCENDENCE][' + otpinstance.user.username + '] OTP code'


    if settings.DEBUG:
        print('OTP:', otpinstance.otp)
        print('USER:', otpinstance.user)

    html_content = 'This is your 4 digits OTP code : <strong>' + str(otpinstance.otp) + '</strong>'
    message = EmailMultiAlternatives(subject, 'This is your 4 digits OTP code : ' + str(otpinstance.otp), None, [otpinstance.user.email])
    message.attach_alternative(html_content, 'text/html')

    try:
        if not settings.DEBUG:
            message.send()
    except SMTPException:
        # Prevent account to be blocked
        instance.is_active = True
        instance.save()
        print('SMTP error (to_email:', instance.email, ')')

@receiver(post_save, sender=OTPInstance)
def send_otp(sender, instance: OTPInstance, created, **kwargs):
    if created:
        send_otp_mail(instance)
