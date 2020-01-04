# Generated by Django 3.0.2 on 2020-01-03 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PremiumCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('new_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_group', to='auth.Group')),
                ('old_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_group', to='auth.Group')),
            ],
        ),
    ]
