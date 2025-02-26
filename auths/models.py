from django.contrib.auth.models import AbstractUser
from django.db import models

# User Model
class User(AbstractUser):
    is_seller = models.BooleanField(default=False)


