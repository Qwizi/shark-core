# Generated by Django 3.0.3 on 2020-02-29 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_auto_20200224_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reaction',
            name='type',
        ),
    ]
