# Generated by Django 3.2.3 on 2021-05-31 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_survey_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
