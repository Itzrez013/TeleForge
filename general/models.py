from django.db import models

# Create your models here.


class Notification(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Security_and_Privacy(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField(max_length=500)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


