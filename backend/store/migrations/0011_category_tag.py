# Generated by Django 3.0.1 on 2019-12-23 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20191223_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='tag',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
    ]