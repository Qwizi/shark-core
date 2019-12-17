# Generated by Django 3.0 on 2019-12-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20191217_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonus',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='options',
            field=models.TextField(default='{}'),
        ),
    ]
