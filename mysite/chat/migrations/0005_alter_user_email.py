# Generated by Django 4.1.3 on 2022-11-30 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_chatmessage_date_time_alter_chatmessage_thread_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=244, unique=True),
        ),
    ]