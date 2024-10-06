from huey import crontab
from huey.contrib.djhuey import db_task, task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

@task()
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    subject = "Verify Your Email"
    message = render_to_string('authentication/verification_email.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject, message, 'no-reply@yourdomain.com', [user.email])

@task()
def send_password_reset_email(user_id):
    user = User.objects.get(id=user_id)
    subject = "Reset Your Password"
    message = render_to_string('authentication/password_reset_email.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject, message, 'no-reply@yourdomain.com', [user.email])
