import uuid

from django.contrib.auth.hashers import identify_hasher, is_password_usable
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.crypto import get_random_string

from shared.restframework.models import BaseModel


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"

