# Generated by Django 3.0.2 on 2020-01-02 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20200102_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bonus_percent',
            field=models.IntegerField(default=1),
        ),
    ]
