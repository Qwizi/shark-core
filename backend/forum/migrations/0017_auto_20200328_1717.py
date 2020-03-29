# Generated by Django 3.0.3 on 2020-03-28 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_auto_20200328_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posts', models.ManyToManyField(to='forum.Post')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Thread')),
            ],
        ),
        migrations.AlterField(
            model_name='reactionitem',
            name='image',
            field=models.URLField(default='http://localhost:3000/images/reactions/thx.png'),
        ),
        migrations.CreateModel(
            name='PromoteAnswer',
            fields=[
                ('bestanswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='forum.BestAnswer')),
            ],
            bases=('forum.bestanswer',),
        ),
    ]