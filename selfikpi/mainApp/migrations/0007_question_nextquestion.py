# Generated by Django 3.1.7 on 2021-04-01 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_questionanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='nextquestion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.question'),
        ),
    ]
