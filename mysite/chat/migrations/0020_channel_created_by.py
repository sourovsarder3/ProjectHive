# Generated by Django 4.1.3 on 2023-02-27 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_channel_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='created_by',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='chat.user'),
        ),
    ]
