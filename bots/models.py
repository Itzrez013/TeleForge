from django.db import models
from accounts.models import User

# Create your models here.


class TelegramBot(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bots"
    )

    token = models.CharField(max_length=255)

    bot_id = models.BigIntegerField(
        unique=True
    )

    username = models.CharField(
        max_length=100,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"{self.name} - {self.owner.email}"