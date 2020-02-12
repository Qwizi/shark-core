# Generated by Django 3.0.3 on 2020-02-12 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0007_auto_20200107_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='thread',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread_author_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
