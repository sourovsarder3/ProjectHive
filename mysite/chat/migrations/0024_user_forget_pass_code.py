# Generated by Django 4.1.7 on 2023-03-31 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0023_imagefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='forget_pass_code',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
