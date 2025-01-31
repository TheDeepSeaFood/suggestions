from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # NOTE: This are not clearly defined as to be of branch or brand
    # this is the reason the type filed is mixed
    USER_TYPE_CHOICES = [
        ("DSF", "Deep Seafood"),
        ("ROF", "Royal Future"),
        ("QAR", "Qatar"),
        ("ABD", "Abu Dhabi"),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2")
        ):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
