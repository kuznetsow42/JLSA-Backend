from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True)
    streak = models.PositiveSmallIntegerField(default=0)

