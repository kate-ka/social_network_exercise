from django.contrib.auth import user_logged_in
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.timezone import now


class User(AbstractUser):
    last_login = models.DateTimeField(null=True)
    last_request = models.DateTimeField(null=True)


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    user.last_login = now()
    user.save(update_fields=["last_login"])
