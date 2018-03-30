# Generated by Django 2.0.3 on 2018-03-30 02:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(max_length=200, unique=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2018, 3, 30, 10, 11, 20, 250275), verbose_name='created date')),
                ('active_date', models.DateTimeField(default=datetime.datetime(2018, 3, 30, 10, 11, 20, 250275), verbose_name='active date')),
                ('status', models.IntegerField(default=0, verbose_name='0:normal,1:frozen,2:suspend,3.deleted')),
            ],
        ),
        migrations.AlterModelOptions(
            name='product',
            options={},
        ),
        migrations.AlterField(
            model_name='product',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 30, 10, 11, 20, 250275), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='product',
            name='expired_date',
            field=models.DateTimeField(null=True, verbose_name='date expired'),
        ),
        migrations.AlterField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.WalletUser'),
        ),
        migrations.AlterField(
            model_name='product',
            name='verify_code',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
