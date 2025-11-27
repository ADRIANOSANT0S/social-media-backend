from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

from apps.core.contracts.lang import ACCEPTED_LANGS


class User(AbstractUser):
    """Custom User model extending AbstractUser."""

    name = models.CharField(
        blank=False, max_length=100, null=False, validators=[MinLengthValidator(2)]
    )
    age = models.IntegerField(
        blank=False, validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    email = models.EmailField(unique=True, blank=False, null=False)
    avatar = models.URLField(blank=True, null=True)
    username = models.CharField(
        max_length=15, unique=True, validators=[MinLengthValidator(3)]
    )
    banner = models.URLField(blank=True, null=True, default=None)
    bio = models.CharField(max_length=150, null=True, blank=True, default=None)
    lang = models.CharField(
        max_length=2,
        choices=ACCEPTED_LANGS,
        default="en",
        blank=False,
    )
    recover_email_code = models.CharField(max_length=150)
    updated_at = models.DateTimeField(auto_now=True)
    is_password_invalidated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ID: {self.id}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["name"]
