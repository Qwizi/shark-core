# Generated by Django 3.0 on 2019-12-15 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('accounts', '0005_auto_20191214_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='display_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]