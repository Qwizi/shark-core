# Generated by Django 3.0.2 on 2020-01-02 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='wallet_type',
            field=models.IntegerField(default=1),
        ),
    ]
