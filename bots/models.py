from django.db import models
from accounts.models import User


class TelegramBot(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bots"
    )

    token = models.CharField(
        max_length=255
    )

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



class BotCommand(models.Model):

    bot = models.ForeignKey(
        TelegramBot,
        on_delete=models.CASCADE,
        related_name="commands"
    )

    name = models.CharField(
        max_length=30
    )

    description = models.CharField(
        max_length=150,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=["bot", "name"],
                name="unique_command_per_bot"
            )

        ]


    def __str__(self):

        return f"{self.name} - {self.bot.name}"


class CommandResponse(models.Model):

    command = models.OneToOneField(
        BotCommand,
        on_delete=models.CASCADE,
        related_name="response"
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return self.command.name