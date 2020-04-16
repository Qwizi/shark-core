# Generated by Django 3.0.3 on 2020-03-28 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0014_auto_20200328_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reactionitem',
            name='image_file',
        ),
        migrations.AlterField(
            model_name='reactionitem',
            name='image_url',
            field=models.URLField(default='http://localhost:8000/static/reactions/thx.png'),
        ),
    ]
