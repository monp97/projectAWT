# Generated by Django 2.1.3 on 2018-11-20 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='startYear',
            field=models.IntegerField(default=2018),
        ),
    ]
