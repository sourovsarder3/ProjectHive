# Generated by Django 4.1.3 on 2023-01-31 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='thread',
            unique_together={('second_person', 'first_person')},
        ),
    ]