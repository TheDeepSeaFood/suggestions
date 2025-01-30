from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

from insights.models import Branch, Brand


class User(AbstractUser):

    branch = models.ForeignKey(Branch, related_name="user_branch", on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, related_name="user_brand", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2")
        ):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
