# Generated by Django 3.1.7 on 2021-03-24 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='textresponse',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
