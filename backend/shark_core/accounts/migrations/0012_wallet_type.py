# Generated by Django 3.0.2 on 2020-01-02 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20191217_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='type',
            field=models.CharField(choices=[(1, 'Podstawowy'), (2, 'Dodatkowy')], default=1, max_length=64, null=True),
        ),
    ]