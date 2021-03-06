# Generated by Django 3.0.1 on 2019-12-30 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('app_id', models.IntegerField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='server',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='servers.Game'),
        ),
    ]
