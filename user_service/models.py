import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from user_service.manager import UserManager


# Create your models here.

class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_instructor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return self.email