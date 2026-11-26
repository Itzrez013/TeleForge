from django.contrib import admin
from .models import TelegramBot,BotCommand,CommandResponse

# Register your models here.


class BotCommadInline(admin.TabularInline):
    model = BotCommand
    fields = None


class CommandResponseInline(admin.TabularInline):
    model = CommandResponse
    fields = None

@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    model = TelegramBot
    inlines = [BotCommadInline,CommandResponseInline]
    list_display = ['owner','username']