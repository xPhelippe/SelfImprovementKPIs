# Generated by Django 3.1.7 on 2021-03-25 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_auto_20210324_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey', to='mainApp.person')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('qtype', models.IntegerField(choices=[(0, 'TEXT'), (1, 'SCALE'), (2, 'YESORNO')])),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='mainApp.survey')),
            ],
        ),
    ]