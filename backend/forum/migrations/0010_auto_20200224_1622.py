# Generated by Django 3.0.3 on 2020-02-24 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0009_auto_20200212_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReactionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('tag', models.CharField(max_length=64, unique=True)),
                ('image', models.ImageField(height_field=64, upload_to='', width_field=64)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Thread'), (2, 'Post')], default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.ReactionItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='reactions',
            field=models.ManyToManyField(to='forum.Reaction'),
        ),
        migrations.AddField(
            model_name='thread',
            name='reactions',
            field=models.ManyToManyField(to='forum.Reaction'),
        ),
    ]