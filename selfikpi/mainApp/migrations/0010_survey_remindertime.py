# Generated by Django 3.2.3 on 2021-05-31 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_person_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='reminderTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
