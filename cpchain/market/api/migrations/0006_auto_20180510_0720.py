# Generated by Django 2.0.3 on 2018-05-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180402_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='Start time'),
        ),
    ]