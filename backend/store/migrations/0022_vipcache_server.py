# Generated by Django 3.0.3 on 2020-03-13 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0006_server_admins'),
        ('store', '0021_vipcache'),
    ]

    operations = [
        migrations.AddField(
            model_name='vipcache',
            name='server',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='servers.Server'),
        ),
    ]
