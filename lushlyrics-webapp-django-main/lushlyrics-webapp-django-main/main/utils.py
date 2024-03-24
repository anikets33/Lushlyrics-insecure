from django.core.mail import send_mail
from django.conf import settings


def send_reset_password_mail(user):
    link = 'http://127.0.0.1:8000//reset_password/{}'.format(user.id)

    subject = "LushLyrics Reset Password"
    message = "Please click on the link to reset password at Lishlyrics is {}".format(link)
    from_mail = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_mail, recipient_list, fail_silently=False)