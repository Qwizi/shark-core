# Generated by Django 3.0 on 2019-12-18 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='status',
            field=models.CharField(choices=[(1, 'Success'), (0, 'Failed')], default=1, max_length=16),
        ),
    ]
