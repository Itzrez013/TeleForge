from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bots", "0006_telegrambot_webhook_secret"),
    ]

    operations = [
        migrations.AlterField(
            model_name="botcommand",
            name="name",
            field=models.CharField(max_length=32),
        ),
    ]
