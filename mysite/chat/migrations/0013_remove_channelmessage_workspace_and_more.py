# Generated by Django 4.1.3 on 2023-02-08 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_channelmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channelmessage',
            name='workspace',
        ),
        migrations.AlterField(
            model_name='channelmessage',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatmessage_thread', to='chat.channel'),
        ),
    ]
