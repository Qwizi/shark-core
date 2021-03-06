# Generated by Django 3.0.3 on 2020-02-15 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_smsnumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('bonuscode', 'Code'), ('sms', 'Sms'), ('transfer', 'Transfer')], default='bonuscode', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='wallet',
            name='payment_methods',
            field=models.ManyToManyField(to='accounts.PaymentType'),
        ),
    ]
